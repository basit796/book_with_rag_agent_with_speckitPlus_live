"""Agent tools for RAG book assistant"""

import json
from pathlib import Path
from typing import List, Dict, Any
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vectordb.store_faiss import FAISSVectorStore
from vectordb.embeddings import generate_embedding


# Load metadata files
METADATA_DIR = Path(__file__).parent.parent / "vectordb"
SUMMARY_METADATA_PATH = METADATA_DIR / "summary_metadata.json"
TOPIC_INDEX_PATH = METADATA_DIR / "topic_index.json"

# Load metadata once at module load
with open(SUMMARY_METADATA_PATH, 'r', encoding='utf-8') as f:
    SUMMARY_METADATA = json.load(f)

with open(TOPIC_INDEX_PATH, 'r', encoding='utf-8') as f:
    TOPIC_INDEX = json.load(f)


def vector_search_tool(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Search the book content using vector similarity.
    
    Args:
        query: The search query text
        top_k: Number of results to return (default 5)
        
    Returns:
        Dictionary containing search results with content and metadata
    """
    try:
        # Generate embedding for the query
        query_embedding = generate_embedding(query, task_type="retrieval_query")
        
        # Search vector database
        store = FAISSVectorStore()
        results = store.search_similar(query_embedding, top_k=top_k)
        # print("results : ",results)
        
        # Format results
        formatted_results = {
            "query": query,
            "results": []
        }
        
        for result in results:
            metadata = result.get("metadata", {})
            formatted_results["results"].append({
                "content": result["content"],
                "source": metadata.get("source", "Unknown"),
                "chapter_title": metadata.get("chapter_title", "Unknown"),
                "module": metadata.get("module_name", "Unknown"),
                "score": result.get("similarity_score", 0.0)
            })

        # print("formatted : ",formatted_results)
        
        return formatted_results
        
    except Exception as e:
        return {
            "error": f"Search failed: {str(e)}",
            "query": query,
            "results": []
        }


def citation_tool(source_path: str) -> Dict[str, Any]:
    """
    Generate proper citation for a book chapter.
    
    Args:
        source_path: File path of the source document
        
    Returns:
        Dictionary containing formatted citation information
    """
    try:
        # Find the chapter in metadata
        for module in SUMMARY_METADATA["modules"]:
            for chapter in module["chapters"]:
                if chapter["file_path"] in source_path or source_path in chapter["file_path"]:
                    return {
                        "citation": f"{module['title']} → {chapter['title']}",
                        "module": module["title"],
                        "module_order": module["order"],
                        "chapter_number": chapter["number"],
                        "chapter_title": chapter["title"],
                        "chapter_id": chapter["id"],
                        "file_path": chapter["file_path"]
                    }
        
        # If not found in metadata, return basic info
        return {
            "citation": f"Source: {source_path}",
            "file_path": source_path,
            "note": "Chapter not found in metadata"
        }
        
    except Exception as e:
        return {
            "error": f"Citation generation failed: {str(e)}",
            "source_path": source_path
        }


def metadata_query_tool(query_type: str, query_value: str = None) -> Dict[str, Any]:
    """
    Query book metadata for navigation and structure information.
    
    Args:
        query_type: Type of query - "list_modules", "list_chapters", "module_info", 
                   "search_topic", "book_stats"
        query_value: Optional value for specific queries (e.g., module id, topic name)
        
    Returns:
        Dictionary containing requested metadata
    """
    try:
        if query_type == "list_modules":
            return {
                "modules": [
                    {
                        "id": m["id"],
                        "title": m["title"],
                        "order": m["order"],
                        "chapter_count": len(m["chapters"]),
                        "word_count": m["word_count"]
                    }
                    for m in SUMMARY_METADATA["modules"]
                ]
            }
        
        elif query_type == "list_chapters":
            all_chapters = []
            for module in SUMMARY_METADATA["modules"]:
                for chapter in module["chapters"]:
                    all_chapters.append({
                        "module": module["title"],
                        "chapter_number": chapter["number"],
                        "title": chapter["title"],
                        "id": chapter["id"],
                        "file_path": chapter["file_path"]
                    })
            return {"chapters": all_chapters}
        
        elif query_type == "module_info" and query_value:
            # Find specific module
            for module in SUMMARY_METADATA["modules"]:
                if module["id"] == query_value or module["title"].lower() in query_value.lower():
                    return {
                        "module": {
                            "id": module["id"],
                            "title": module["title"],
                            "order": module["order"],
                            "description": module["description"],
                            "word_count": module["word_count"],
                            "chapters": [
                                {
                                    "number": ch["number"],
                                    "title": ch["title"],
                                    "id": ch["id"],
                                    "topics": ch["topics"][:5]  # First 5 topics
                                }
                                for ch in module["chapters"]
                            ]
                        }
                    }
            return {"error": f"Module not found: {query_value}"}
        
        elif query_type == "search_topic" and query_value:
            # Search for topic in index
            matching_topics = {}
            query_lower = query_value.lower()
            
            for topic, data in TOPIC_INDEX["topics"].items():
                if query_lower in topic.lower():
                    matching_topics[topic] = {
                        "chapters": data["chapters"],
                        "description": data["description"]
                    }
            
            return {
                "query": query_value,
                "matching_topics": matching_topics,
                "count": len(matching_topics)
            }
        
        elif query_type == "book_stats":
            return {
                "statistics": {
                    "total_modules": SUMMARY_METADATA["total_modules"],
                    "total_chapters": SUMMARY_METADATA["total_chapters"],
                    "total_words": SUMMARY_METADATA["total_words"],
                    "total_topics": len(TOPIC_INDEX["topics"]),
                    "modules": [
                        {
                            "title": m["title"],
                            "chapters": len(m["chapters"]),
                            "words": m["word_count"]
                        }
                        for m in SUMMARY_METADATA["modules"]
                    ]
                }
            }
        
        else:
            return {
                "error": f"Unknown query type: {query_type}",
                "supported_types": [
                    "list_modules", "list_chapters", "module_info", 
                    "search_topic", "book_stats"
                ]
            }
            
    except Exception as e:
        return {
            "error": f"Metadata query failed: {str(e)}",
            "query_type": query_type,
            "query_value": query_value
        }


# Tool descriptions for agent registration
TOOL_DESCRIPTIONS = {
    "vector_search": {
        "name": "vector_search",
        "description": "Search the book content using semantic similarity. Use this to find relevant information about physical AI, robotics, ROS2, simulation, or Isaac platform.",
        "parameters": {
            "query": "The search query text",
            "top_k": "Number of results to return (default 5)"
        }
    },
    "citation": {
        "name": "citation",
        "description": "Generate a properly formatted citation for a book chapter. Use this to provide source attribution for information.",
        "parameters": {
            "source_path": "File path of the source document"
        }
    },
    "metadata_query": {
        "name": "metadata_query",
        "description": "Query book structure and navigation metadata. Use this to list modules, chapters, search topics, or get book statistics.",
        "parameters": {
            "query_type": "Type of query: list_modules, list_chapters, module_info, search_topic, book_stats",
            "query_value": "Optional value for specific queries (module id, topic name, etc.)"
        }
    }
}


if __name__ == "__main__":
    # Test the tools
    print("=== Testing Agent Tools ===\n")
    
    # Test 1: Vector search
    print("1. Testing vector_search_tool...")
    result = vector_search_tool("Robots Need Middleware?", top_k=3)
    print("result : ",result)
    print(f"   Found {len(result.get('results', []))} results")
    if result.get('results'):
        print(f"   Top result from: {result['results'][0]['source']}")
    
    # Test 2: Citation
    print("\n2. Testing citation_tool...")
    citation = citation_tool("docs/module-1-physical-ai/01-what-is-physical-ai.md")
    print("citation : ",citation)
    print(f"   Citation: {citation.get('citation', 'N/A')}")
    
    # Test 3: Metadata queries
    print("\n3. Testing metadata_query_tool...")
    modules = metadata_query_tool("list_modules")
    print("   Modules : ",modules)
    print(f"   Found {len(modules.get('modules', []))} modules")
    
    stats = metadata_query_tool("book_stats")
    print(f"   Book stats: {stats.get('statistics', {}).get('total_chapters', 0)} chapters")
    print("stats : ",stats )
    
    print("\n✅ All tool tests completed!")
