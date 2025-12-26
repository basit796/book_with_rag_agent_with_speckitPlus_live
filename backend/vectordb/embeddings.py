"""Google Gemini embedding generation"""

import os
import time
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=API_KEY)


def generate_embedding(text: str, task_type: str = "retrieval_document", max_retries: int = 3) -> List[float]:
    """
    Generate embedding for text using Gemini text-embedding-004.
    
    Args:
        text: Text to embed
        task_type: "retrieval_document" for indexing, "retrieval_query" for search
        max_retries: Maximum retry attempts
        
    Returns:
        List of 768 floating point numbers
    """
    for attempt in range(max_retries):
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type=task_type
            )
            return result['embedding']
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Embedding failed (attempt {attempt + 1}/{max_retries}): {e}")
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise Exception(f"Failed to generate embedding after {max_retries} attempts: {e}")


def generate_query_embedding(query: str) -> List[float]:
    """Generate embedding for search query."""
    return generate_embedding(query, task_type="retrieval_query")


def generate_batch_embeddings(texts: List[str], task_type: str = "retrieval_document", 
                              batch_size: int = 100) -> List[List[float]]:
    """
    Generate embeddings for multiple texts in batches.
    
    Args:
        texts: List of texts to embed
        task_type: Embedding task type
        batch_size: Number of texts per batch (max 100)
        
    Returns:
        List of embeddings
    """
    embeddings = []
    total = len(texts)
    
    for i in range(0, total, batch_size):
        batch = texts[i:i+batch_size]
        print(f"Generating embeddings for batch {i//batch_size + 1} ({i+1}-{min(i+batch_size, total)} of {total})")
        
        try:
            # Gemini supports batch embedding
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=batch,
                task_type=task_type
            )
            
            # Handle single vs batch results
            if isinstance(result['embedding'][0], list):
                embeddings.extend(result['embedding'])
            else:
                embeddings.append(result['embedding'])
                
        except Exception as e:
            print(f"Batch embedding failed: {e}")
            # Fallback to individual embedding
            for text in batch:
                try:
                    emb = generate_embedding(text, task_type)
                    embeddings.append(emb)
                except Exception as inner_e:
                    print(f"Individual embedding failed: {inner_e}")
                    # Use zero vector as fallback
                    embeddings.append([0.0] * 768)
        
        # Rate limiting: small delay between batches
        if i + batch_size < total:
            time.sleep(1)
    
    return embeddings


if __name__ == "__main__":
    # Test embedding generation
    test_text = "Physical AI combines artificial intelligence with physical embodiment in robots."
    
    print("Generating document embedding...")
    doc_embedding = generate_embedding(test_text)
    print(f"Embedding dimension: {len(doc_embedding)}")
    print(f"First 5 values: {doc_embedding[:5]}")
    
    print("\nGenerating query embedding...")
    query_embedding = generate_query_embedding("What is physical AI?")
    print(f"Embedding dimension: {len(query_embedding)}")
    print(f"First 5 values: {query_embedding[:5]}")
