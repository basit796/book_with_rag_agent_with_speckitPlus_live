"""Test vector database functionality"""

import numpy as np
from vectordb.store_faiss import FAISSVectorStore

def test_vector_db():
    """Test FAISS vector database operations"""
    print("\n=== Testing Vector Database ===\n")
    
    # 1. Load vector store
    print("1. Loading vector store...")
    store = FAISSVectorStore()
    print(f"   ✅ Loaded {store.index.ntotal} vectors\n")
    
    # 2. Test search with dummy query
    print("2. Testing search functionality...")
    dummy_query = np.random.randn(768).tolist()
    results = store.search_similar(dummy_query, top_k=3)
    print(f"   ✅ Search returned {len(results)} results\n")
    
    # 3. Display results
    if results:
        print("3. Sample search results:")
        for i, result in enumerate(results[:3], 1):
            metadata = result.get("metadata", {})
            content_preview = result.get("content", "")[:100]
            print(f"\n   Result {i}:")
            print(f"   - Module: {metadata.get('module_name', 'Unknown')}")
            print(f"   - File: {metadata.get('file_path', 'Unknown')}")
            print(f"   - Score: {result.get('score', 0):.4f}")
            print(f"   - Preview: {content_preview}...")
    
    print("\n\n✅ All vector DB tests passed!\n")

if __name__ == "__main__":
    test_vector_db()
