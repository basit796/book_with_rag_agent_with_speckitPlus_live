"""Agent runner for orchestrating RAG queries"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from agent import BookAgent


class AgentRunner:
    """Orchestrates agent execution with conversation state management"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Initialize the agent runner.
        
        Args:
            model_name: Gemini model to use
        """
        self.agent = BookAgent(model_name=model_name)
        self.conversation_history = []
    
    def run(self, user_query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Run the agent with a user query.
        
        Args:
            user_query: User's question or request
            session_id: Optional session identifier
            
        Returns:
            Dictionary with answer, citations, and metadata
        """
        # Add query to history
        self.conversation_history.append({
            "role": "user",
            "content": user_query
        })
        
        # Get response from agent
        result = self.agent.query(user_query)
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": result["response"]
        })
        
        # Transform to API format
        citations = []
        for source in result.get("sources", []):
            citations.append({
                "chapter": source.get("chapter_title", "Unknown"),
                "section": source.get("section_heading"),
                "module": source.get("module_name")
            })
        
        return {
            "answer": result["response"],
            "citations": citations,
            "session_id": session_id or "default",
            "conversation_id": len(self.conversation_history) // 2
        }
    
    def chat(self, user_query: str) -> str:
        """
        Simple chat interface.
        
        Args:
            user_query: User's question
            
        Returns:
            Response text with citations
        """
        result = self.run(user_query)
        return result["response"]
    
    def get_history(self, last_n: Optional[int] = None) -> list:
        """
        Get conversation history.
        
        Args:
            last_n: Number of recent messages to return (None for all)
            
        Returns:
            List of conversation messages
        """
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get runner statistics including vector database stats"""
        stats = {
            "total_messages": len(self.conversation_history),
            "total_conversations": len(self.conversation_history) // 2,
            "model": self.agent.model.model_name if hasattr(self.agent.model, 'model_name') else "gemini-2.5-flash"
        }
        
        # Add vector database statistics
        try:
            metadata_dir = Path(__file__).parent.parent / "vectordb"
            summary_path = metadata_dir / "summary_metadata.json"
            topic_path = metadata_dir / "topic_index.json"
            
            if summary_path.exists():
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary = json.load(f)
                    stats["total_chunks"] = summary.get("total_chunks", 0)
                    stats["modules"] = summary.get("total_modules", 0)
                    stats["chapters"] = summary.get("total_chapters", 0)
            
            if topic_path.exists():
                with open(topic_path, 'r', encoding='utf-8') as f:
                    topics = json.load(f)
                    stats["topics"] = len(topics.get("topics", {}))
        except Exception:
            # If metadata files don't exist, use defaults
            stats["total_chunks"] = 0
            stats["modules"] = 0
            stats["chapters"] = 0
            stats["topics"] = 0
        
        return stats


def run_agent(query: str, model_name: str = "gemini-2.5-flash") -> Dict[str, Any]:
    """
    Convenience function to run agent with a single query.
    
    Args:
        query: User query
        model_name: Gemini model to use
        
    Returns:
        Agent response dictionary
    """
    runner = AgentRunner(model_name=model_name)
    return runner.run(query)


if __name__ == "__main__":
    # Test the runner
    print("=== Testing Agent Runner ===\n")
    
    runner = AgentRunner()
    
    # Test 1: Single query
    print("1. Single Query Test")
    result = runner.run("What is physical AI?")
    print("result:  ", result)
    print(f"   Response length: {len(result['response'])} chars")
    print(f"   Sources: {len(result.get('sources', []))}")
    print(f"   Conversation ID: {result.get('conversation_id')}")
    
    # Test 2: Follow-up query
    print("\n2. Follow-up Query Test")
    result = runner.run("What are the main modules in the book?")
    print(f"   Response length: {len(result['response'])} chars")
    print(f"   Conversation ID: {result.get('conversation_id')}")
    
    # Test 3: History
    print("\n3. Conversation History")
    history = runner.get_history()
    print(f"   Total messages: {len(history)}")
    print(f"   First message: {history[0]['content'][:50]}...")
    
    # Test 4: Statistics
    print("\n4. Runner Statistics")
    stats = runner.get_statistics()
    print(f"   {stats}")
    
    # Test 5: Convenience function
    print("\n5. Convenience Function Test")
    result = run_agent("List all modules")
    print(f"   Response length: {len(result['response'])} chars")
    
    print("\n✅ Runner tests completed!")
