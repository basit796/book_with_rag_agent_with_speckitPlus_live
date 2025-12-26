"""FAISS vector store operations"""

import os
import json
import pickle
from typing import List, Dict, Any, Optional
import numpy as np
import faiss
from pathlib import Path


class FAISSVectorStore:
    """FAISS vector store for book content vectors"""
    
    def __init__(self, persist_directory: Optional[str] = None, embedding_dim: int = 768):
        """
        Initialize FAISS index and metadata storage.
        
        Args:
            persist_directory: Directory to persist the database
            embedding_dim: Dimension of embeddings (768 for text-embedding-004)
        """
        if persist_directory is None:
            persist_directory = os.getenv(
                "VECTOR_DB_DIRECTORY",
                str(Path(__file__).parent / "vector_db")
            )
        
        # Ensure directory exists
        self.persist_dir = Path(persist_directory)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        
        self.embedding_dim = embedding_dim
        self.index_path = self.persist_dir / "faiss.index"
        self.metadata_path = self.persist_dir / "metadata.pkl"
        
        # Initialize or load FAISS index
        if self.index_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            print(f"✅ FAISS index loaded with {self.index.ntotal} documents")
        else:
            # Create new index (L2 distance with flat index)
            self.index = faiss.IndexFlatL2(embedding_dim)
            self.metadata = []
            print(f"✅ New FAISS index created (dim={embedding_dim})")
    
    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Add chunks to the collection.
        
        Args:
            chunks: List of chunk dictionaries with 'id', 'content', 'metadata'
            embeddings: List of embedding vectors
        """
        if len(chunks) != len(embeddings):
            raise ValueError(f"Chunks ({len(chunks)}) and embeddings ({len(embeddings)}) must have same length")
        
        # Extract data
        ids = [chunk["id"] for chunk in chunks]
        documents = [chunk["content"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        
        # Add to collection in batches (ChromaDB recommends batch size of 41666)
        batch_size = 1000
        for i in range(0, len(ids), batch_size):
            batch_end = min(i + batch_size, len(ids))
            print(f"Adding batch {i//batch_size + 1}: documents {i+1}-{batch_end} of {len(ids)}")
            
            self.collection.add(
                ids=ids[i:batch_end],
                embeddings=embeddings[i:batch_end],
                documents=documents[i:batch_end],
                metadatas=metadatas[i:batch_end]
            )
        
        print(f"Successfully added {len(chunks)} chunks to ChromaDB")
    
    def search_similar(self, query_embedding: List[float], top_k: int = 5,
                      filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar chunks using vector similarity.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_metadata: Optional metadata filters (e.g., {"module_name": "module-1-physical-ai"})
            
        Returns:
            List of results with content, metadata, and similarity score
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["ids"][0])):
            distance = results["distances"][0][i]
            similarity = 1 - distance  # Convert distance to similarity
            
            # Filter by similarity threshold
            if similarity >= 0.5:  # Only return reasonably similar results
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity_score": similarity
                })
        
        return formatted_results
    
    def get_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific chunk by ID."""
        try:
            result = self.collection.get(
                ids=[chunk_id],
                include=["documents", "metadatas"]
            )
            if result["ids"]:
                return {
                    "id": result["ids"][0],
                    "content": result["documents"][0],
                    "metadata": result["metadatas"][0]
                }
        except Exception as e:
            print(f"Error retrieving chunk {chunk_id}: {e}")
        return None
    
    def count(self) -> int:
        """Get total number of chunks in collection."""
        return self.collection.count()
    
    def reset(self):
        """Delete all data in the collection."""
        self.client.delete_collection("book_chapters")
        self.collection = self.client.get_or_create_collection(
            name="book_chapters",
            metadata={
                "description": "Physical AI & Humanoid Robotics book content",
                "embedding_model": "text-embedding-004",
                "embedding_dimensions": 768
            }
        )
        print("Collection reset successfully")


if __name__ == "__main__":
    # Test store operations
    store = ChromaDBStore()
    print(f"Current document count: {store.count()}")
