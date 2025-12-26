"""Build vector index from book content"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vectordb.chunker import chunk_markdown_files
from vectordb.embeddings import generate_batch_embeddings
from vectordb.store_faiss import FAISSVectorStore
from vectordb.metadata_builder import build_metadata

load_dotenv()





def build_index():
    """Main function to build the vector index with FAISS."""
    print("=== Building Vector Index with FAISS ===\n")
    
    # Step 1: Chunk markdown files
    print("Step 1: Chunking markdown files...")
    docs_dir = Path(__file__).parent.parent.parent / "Future Ai And Robotics" / "docs"
    chunks = chunk_markdown_files(docs_dir)
    
    if not chunks:
        print("❌ Error: No chunks created")
        return
    
    print(f"✅ Created {len(chunks)} chunks")
    
    # Step 2: Generate embeddings
    print("\nStep 2: Generating embeddings...")
    texts = [chunk["content"] for chunk in chunks]
    embeddings = generate_batch_embeddings(texts, task_type="retrieval_document", batch_size=50)
    
    if len(embeddings) != len(chunks):
        print(f"❌ Warning: Embedding count ({len(embeddings)}) != chunk count ({len(chunks)})")
        return
    
    print(f"✅ Generated {len(embeddings)} embeddings")
    
    # Step 3: Store in FAISS
    print("\nStep 3: Storing in FAISS vector database...")
    store = FAISSVectorStore()
    
    # Reset existing data if needed
    if store.count() > 0:
        print(f"⚠️  Collection has {store.count()} documents.")
        store.reset()
    
    store.add_chunks(chunks, embeddings)
    print(f"✅ FAISS index built with {store.count()} chunks")
    
    # Step 4: Generate metadata
    print("\nStep 4: Generating metadata files...")
    metadata_dir = Path(__file__).parent
    summary, topic_index = build_metadata(docs_dir, metadata_dir)
    
    # Summary
    print("\n=== Index Build Complete ===")
    print(f"📊 Statistics:")
    print(f"  - Total chunks: {len(chunks)}")
    print(f"  - Total modules: {summary['total_modules']}")
    print(f"  - Total chapters: {summary['total_chapters']}")
    print(f"  - Total words: {summary['total_words']:,}")
    print(f"  - FAISS index size: {store.count()} vectors")
    print(f"  - Unique topics: {len(topic_index['topics'])}")
    print(f"\n✅ Vector database and metadata ready!")


if __name__ == "__main__":
    build_index()
