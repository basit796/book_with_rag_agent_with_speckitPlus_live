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
        Add chunks to the index.
        
        Args:
            chunks: List of chunk dictionaries with 'id', 'content', 'metadata'
            embeddings: List of embedding vectors
        """
        if len(chunks) != len(embeddings):
            raise ValueError(f"Chunks ({len(chunks)}) and embeddings ({len(embeddings)}) must have same length")
        
        # Convert embeddings to numpy array
        embeddings_array = np.array(embeddings, dtype=np.float32)
        
        # Add to FAISS index
        self.index.add(embeddings_array)
        
        # Store metadata
        for chunk in chunks:
            self.metadata.append({
                "id": chunk["id"],
                "content": chunk["content"],
                "metadata": chunk["metadata"]
            })
        
        print(f"✅ Successfully added {len(chunks)} chunks to FAISS index")
        self._save()
    
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
        if self.index.ntotal == 0:
            print("⚠️  Index is empty")
            return []
        
        # Convert query to numpy array
        query_array = np.array([query_embedding], dtype=np.float32)
        
        # Search FAISS index
        distances, indices = self.index.search(query_array, min(top_k * 2, self.index.ntotal))
        
        # Format results
        formatted_results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx == -1:  # FAISS returns -1 for empty slots
                continue
            
            # Get metadata
            chunk_meta = self.metadata[idx]
            
            # Apply metadata filter if provided
            if filter_metadata:
                match = all(
                    chunk_meta["metadata"].get(k) == v 
                    for k, v in filter_metadata.items()
                )
                if not match:
                    continue
            
            # Convert L2 distance to similarity score (inverse)
            # Normalize: smaller distance = higher similarity
            similarity = 1 / (1 + dist)
            
            # Filter by similarity threshold
            if similarity >= 0.3:  # Reasonable threshold
                formatted_results.append({
                    "id": chunk_meta["id"],
                    "content": chunk_meta["content"],
                    "metadata": chunk_meta["metadata"],
                    "similarity_score": float(similarity)
                })
            
            # Break if we have enough results
            if len(formatted_results) >= top_k:
                break
        
        return formatted_results
    
    def get_by_id(self, chunk_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific chunk by ID."""
        for chunk in self.metadata:
            if chunk["id"] == chunk_id:
                return chunk
        return None
    
    def count(self) -> int:
        """Get total number of chunks in index."""
        return self.index.ntotal
    
    def reset(self):
        """Delete all data in the index."""
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.metadata = []
        self._save()
        print("✅ Index reset successfully")
    
    def _save(self):
        """Save index and metadata to disk."""
        faiss.write_index(self.index, str(self.index_path))
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        print(f"💾 Index saved to {self.persist_dir}")


if __name__ == "__main__":
    # Test store operations
    store = FAISSVectorStore()
    print(f"Current document count: {store.count()}")
