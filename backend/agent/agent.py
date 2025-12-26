"""Book RAG Agent using Google Gemini"""

import os
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv

from .tools import vector_search_tool, citation_tool, metadata_query_tool

load_dotenv()


class BookAgent:
    """RAG Agent for Physical AI & Robotics Book"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        """
        Initialize the Book Agent with Gemini model.
        
        Args:
            model_name: Name of the Gemini model to use
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        self.system_prompt = """You are an expert assistant for the book "Physical AI & Humanoid Robotics: A Comprehensive Guide to Building Intelligent Physical Systems."

Your role is to help users understand concepts from the book, which covers:
- Module 1: Physical AI Foundations (4 chapters)
- Module 2: ROS2 Middleware (4 chapters)  
- Module 3: Simulation & Digital Twins (4 chapters)
- Module 4: NVIDIA Isaac Platform (4 chapters)

**Available Tools:**
1. **vector_search**: Search book content semantically
2. **citation**: Generate proper chapter citations
3. **metadata_query**: Query book structure and navigation

**Guidelines:**
- Always search for information using vector_search before answering
- Provide citations for information from the book
- Be helpful, accurate, and concise
- If a topic is in the book, find it; if not, say so clearly
- Use metadata_query to help users navigate the book structure
- Format answers clearly with proper structure

**Response Format:**
- Give clear, well-structured answers
- Include citations in format: "Module X → Chapter Y: Title"
- For navigation queries, list modules/chapters clearly
- Admit uncertainty if information is not in the book"""

    def _execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name with given parameters"""
        if tool_name == "vector_search":
            return vector_search_tool(**kwargs)
        elif tool_name == "citation":
            return citation_tool(**kwargs)
        elif tool_name == "metadata_query":
            return metadata_query_tool(**kwargs)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def _format_search_results(self, results: Dict[str, Any]) -> str:
        """Format vector search results for context"""
        if not results.get("results"):
            return "No relevant content found."
        
        formatted = "**Relevant Content from Book:**\n\n"
        for i, result in enumerate(results["results"][:3], 1):  # Top 3 results
            formatted += f"{i}. **{result.get('chapter_title', 'Unknown Chapter')}**\n"
            formatted += f"   Module: {result.get('module', 'Unknown')}\n"
            formatted += f"   Content: {result['content'][:300]}...\n"
            formatted += f"   Source: {result['source']}\n\n"
        return formatted
    
    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query and return a response with citations.
        
        Args:
            user_query: The user's question or request
            
        Returns:
            Dictionary containing response, citations, and sources
        """
        try:
            # Step 1: Determine if we need to search or just query metadata
            query_lower = user_query.lower()
            
            # Check if it's a navigation/structure query
            if any(word in query_lower for word in ["module", "chapter", "list", "what chapters", "how many"]):
                # Use metadata query
                if "list" in query_lower and "module" in query_lower:
                    metadata = self._execute_tool("metadata_query", query_type="list_modules")
                elif "list" in query_lower and "chapter" in query_lower:
                    metadata = self._execute_tool("metadata_query", query_type="list_chapters")
                elif "stats" in query_lower or "how many" in query_lower:
                    metadata = self._execute_tool("metadata_query", query_type="book_stats")
                else:
                    # Search for specific module/topic
                    metadata = self._execute_tool("metadata_query", query_type="search_topic", query_value=user_query)
                
                # Generate response using metadata
                prompt = f"{self.system_prompt}\n\nUser Query: {user_query}\n\nMetadata: {metadata}\n\nProvide a clear, helpful response."
                response = self.model.generate_content(prompt)
                
                return {
                    "response": response.text,
                    "sources": [],
                    "metadata": metadata
                }
            
            # Step 2: Content search query - use vector search
            search_results = self._execute_tool("vector_search", query=user_query, top_k=5)
            
            if not search_results.get("results"):
                return {
                    "response": "I couldn't find relevant information about that topic in the book. Could you rephrase your question or ask about a different topic?",
                    "sources": [],
                    "search_results": search_results
                }
            
            # Step 3: Format context and generate response
            context = self._format_search_results(search_results)
            
            prompt = f"""{self.system_prompt}

**Context from Book:**
{context}

**User Query:** {user_query}

**Instructions:**
- Use the context provided to answer the question
- Include citations in format: "Module X → Chapter Y: Title"
- Be specific and accurate
- If the context doesn't fully answer the question, acknowledge that"""

            response = self.model.generate_content(prompt)
            
            # Step 4: Extract sources for citations
            sources = []
            for result in search_results["results"][:3]:
                citation = self._execute_tool("citation", source_path=result["source"])
                if not citation.get("error"):
                    sources.append(citation)
            
            return {
                "response": response.text,
                "sources": sources,
                "search_results": search_results
            }
            
        except Exception as e:
            return {
                "response": f"I encountered an error processing your query: {str(e)}",
                "sources": [],
                "error": str(e)
            }
    
    def chat(self, user_query: str) -> str:
        """
        Simple chat interface that returns just the response text.
        
        Args:
            user_query: The user's question
            
        Returns:
            Response text as string
        """
        result = self.query(user_query)
        response = result["response"]
        
        # Append citations if available
        if result.get("sources"):
            response += "\n\n**Sources:**\n"
            for source in result["sources"]:
                response += f"- {source['citation']}\n"
        
        return response


if __name__ == "__main__":
    # Test the agent
    print("=== Testing Book Agent ===\n")
    
    agent = BookAgent()
    
    # Test 1: Content query
    print("1. Content Query: 'What is physical AI?'")
    result = agent.query("hi what information you have")
    print(f"   Response preview: {result['response'][:200]}...")
    print(f"   Sources: {len(result.get('sources', []))}")
    
    # Test 2: Navigation query
    print("\n2. Navigation Query: 'List all modules'")
    result = agent.query("List all modules in the book")
    print(f"   Response preview: {result['response'][:200]}...")
    
    # Test 3: Chat interface
    print("\n3. Chat Interface: 'What topics does module 2 cover?'")
    response = agent.chat("What topics does module 2 cover?")
    print(f"   Chat response preview: {response[:200]}...")
    
    print("\n✅ Agent tests completed!")
