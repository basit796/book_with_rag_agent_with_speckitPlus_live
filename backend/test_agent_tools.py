"""Test agent tools functionality"""

import os
from agent.tools import vector_search_tool, citation_tool, metadata_query_tool

def test_agent_tools():
    """Test all agent tools"""
    print("\n=== Testing Agent Tools ===\n")
    
    # Test 1: Vector Search Tool
    print("1. Testing vector_search_tool...")
    print("   Query: 'What is Physical AI?'")
    try:
        search_results = vector_search_tool("What is Physical AI?", top_k=3)
        print(f"   ✅ Search completed")
        print(f"   Found {len(search_results)} results\n")
        if search_results:
            print(f"   First result preview:")
            print(f"   {search_results[0][:200]}...\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Test 2: Citation Tool
    print("2. Testing citation_tool...")
    try:
        citations = citation_tool([
            {"file_path": "docs/module-1-physical-ai/what-is-physical-ai.md"},
            {"file_path": "docs/module-2-ros2/architecture.md"}
        ])
        print(f"   ✅ Citations generated:")
        print(f"   {citations}\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Test 3: Metadata Query Tool
    print("3. Testing metadata_query_tool...")
    try:
        # Test module query
        result = metadata_query_tool("What chapters are in module 1?")
        print(f"   ✅ Query: 'What chapters are in module 1?'")
        print(f"   Result: {result[:200]}...\n")
        
        # Test topic query
        result2 = metadata_query_tool("Which chapters discuss ROS 2?")
        print(f"   ✅ Query: 'Which chapters discuss ROS 2?'")
        print(f"   Result: {result2[:200]}...\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    print("✅ All tool tests completed!\n")

if __name__ == "__main__":
    # Check API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY not set. Some tests may fail.")
    
    test_agent_tools()
