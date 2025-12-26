# Research: RAG Agent System Implementation

**Feature**: Book Content Migration & RAG Chatbot Integration
**Date**: 2025-12-25
**Researcher**: AI Agent
**Status**: Complete

## Executive Summary

This research document consolidates findings on implementing a RAG (Retrieval-Augmented Generation) chatbot system using Google ADK (Agent Development Kit), ChromaDB for vector storage, and Gemini embeddings. The system will enable semantic search across 16 chapters of Physical AI & Humanoid Robotics content integrated into a Docusaurus site.

## R1: Google ADK (Agent Development Kit) Architecture

### Decision: Use google-adk with LlmAgent pattern

**Architecture Pattern:**
```python
from google.generativeai.types import Agent, Tool

# Define tools
search_tool = Tool(
    name="vector_search",
    description="Search book content using semantic similarity",
    function=vector_search_function
)

citation_tool = Tool(
    name="format_citation",
    description="Format source citations from retrieved chunks",
    function=format_citation_function
)

metadata_tool = Tool(
    name="query_metadata",
    description="Query book structure (modules, chapters, topics)",
    function=query_metadata_function
)

# Create agent
agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    tools=[search_tool, citation_tool, metadata_tool],
    system_instruction="You are a helpful assistant for the Physical AI & Humanoid Robotics book..."
)
```

**Rationale:**
- **ADK Compliance**: Follows Google's recommended agent architecture pattern
- **Modular Tools**: Each tool has single responsibility (search, citation, metadata)
- **Testability**: Tools can be unit tested independently
- **Extensibility**: Easy to add new tools (e.g., glossary lookup, code example search)
- **Integration**: Native support for Gemini models

**Tool Execution Flow:**
1. User submits question via chat widget
2. Agent receives question and determines which tool(s) to use
3. Tools execute (vector search, metadata query, etc.)
4. Agent synthesizes results into natural language response
5. Citations are formatted and attached
6. Response returned to frontend

**File Structure:**
```
backend/agent/
├── __init__.py          # Package initialization
├── agent.py             # LlmAgent setup and configuration
├── tools.py             # Tool function implementations
└── runner.py            # Agent orchestration and execution
```

**Alternatives Considered:**
- **LangChain**: More complex, additional dependency, not ADK-compliant
- **Custom Agent Loop**: Reinventing the wheel, harder to maintain
- **OpenAI Assistants API**: Requires OpenAI (spec requires Google Gemini)

### ADK Installation

```bash
pip install google-adk==1.15.0
pip install google-generativeai==1.36.0
```

**Version Rationale:**
- google-adk 1.15.0: Latest stable with LlmAgent support
- google-generativeai 1.36.0: Required for Gemini 2.0 models

---

## R2: Google Gemini API Integration

### Decision: Use text-embedding-004 for embeddings, gemini-2.0-flash-exp for generation

**Embedding Model: text-embedding-004**
- **Dimensions**: 768 (default output size)
- **Max Input**: 2048 tokens per request
- **Batch Support**: Up to 100 embeddings per batch
- **Cost**: Free tier: 1,500 requests/day

**Generation Model: gemini-2.0-flash-exp**
- **Context Window**: 1M tokens (sufficient for book content)
- **Output**: 8,192 tokens max
- **Speed**: ~1-2 seconds per response
- **Cost**: Free tier during experimental phase

**API Authentication Pattern:**
```python
import google.generativeai as genai
import os

# Load API key from environment
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Generate embedding
def generate_embedding(text: str) -> list[float]:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document"  # Optimized for document indexing
    )
    return result['embedding']

# For queries, use different task_type
def generate_query_embedding(text: str) -> list[float]:
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_query"  # Optimized for search queries
    )
    return result['embedding']
```

**Rate Limits & Error Handling:**
```python
from google.api_core.exceptions import ResourceExhausted, DeadlineExceeded
import time

def generate_embedding_with_retry(text: str, max_retries: int = 3) -> list[float]:
    for attempt in range(max_retries):
        try:
            return generate_embedding(text)
        except ResourceExhausted:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
        except DeadlineExceeded:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                raise
```

**Cost Estimation:**
- **One-time indexing**: ~300 chunks × 1 embedding = 300 requests (well within free tier)
- **Query embeddings**: ~10-50 per day per user (free tier sufficient)
- **Generation**: ~10-50 responses per day (free tier sufficient)
- **Total cost**: $0 (free tier adequate for development and initial deployment)

**Environment Configuration (.env):**
```bash
GEMINI_API_KEY=your_api_key_here
GEMINI_EMBEDDING_MODEL=models/text-embedding-004
GEMINI_GENERATION_MODEL=gemini-2.0-flash-exp
```

**Alternatives Considered:**
- **OpenAI embeddings**: Ruled out (spec requires Google Gemini)
- **Local embeddings (sentence-transformers)**: Lower quality, larger deployment size
- **Vertex AI**: More complex setup, requires GCP project

---

## R3: ChromaDB for Vector Storage

### Decision: Use ChromaDB with persistent local storage

**Collection Design:**
```python
import chromadb
from chromadb.config import Settings

# Initialize client with persistent storage
client = chromadb.Client(Settings(
    persist_directory="./backend/vectordb/chroma_db",
    anonymized_telemetry=False
))

# Create collection
collection = client.create_collection(
    name="book_chapters",
    metadata={
        "description": "Physical AI & Humanoid Robotics book content",
        "embedding_model": "text-embedding-004",
        "embedding_dimensions": 768
    }
)
```

**Metadata Schema for Chunks:**
```python
chunk_metadata = {
    "module_name": "module-1-physical-ai",  # Directory name
    "module_title": "Physical AI Foundations",  # Human-readable
    "chapter_number": 1,
    "chapter_id": "01-introduction",  # File name without .md
    "chapter_title": "Introduction to Physical AI",
    "section_heading": "1.2 Key Concepts",  # Section within chapter
    "file_path": "docs/module-1-physical-ai/01-introduction.md",
    "chunk_index": 0,  # Position within chapter
    "word_count": 234,
    "has_code_blocks": False,
    "has_images": True
}
```

**Adding Documents:**
```python
def add_chunks_to_collection(chunks: list[dict], embeddings: list[list[float]]):
    collection.add(
        ids=[chunk["id"] for chunk in chunks],  # Unique ID per chunk
        embeddings=embeddings,
        metadatas=[chunk["metadata"] for chunk in chunks],
        documents=[chunk["content"] for chunk in chunks]
    )
```

**Query Pattern for Top-K Similarity Search:**
```python
def search_similar_chunks(query_embedding: list[float], top_k: int = 5) -> dict:
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    
    # Filter by similarity threshold (distance < 0.3 is good match)
    filtered_results = []
    for i, distance in enumerate(results["distances"][0]):
        if distance < 0.5:  # Cosine distance threshold
            filtered_results.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "similarity_score": 1 - distance  # Convert to similarity
            })
    
    return filtered_results
```

**Persistence Configuration:**
- **Storage**: Local directory `backend/vectordb/chroma_db/`
- **Backup**: Entire directory can be version controlled (Git LFS) or copied
- **Size Estimate**: ~10-20 MB for 300 chunks (embeddings + metadata)

**Alternatives Considered:**
- **Pinecone**: Cloud-only, requires API key, costs money after free tier
- **Weaviate**: More complex setup, overkill for 300 chunks
- **FAISS**: Lower-level, no metadata support, harder to use
- **Qdrant**: Similar to ChromaDB but less Python-native

**Rationale for ChromaDB:**
- **Local-first**: No external dependencies, works offline
- **Python-native**: Simple API, good documentation
- **Metadata support**: First-class support for rich metadata
- **Persistence**: Built-in persistent storage
- **Performance**: Fast enough for <500 chunks (<500ms retrieval)

---

## R4: Markdown Chunking Strategy

### Decision: Semantic chunking with 500-1000 tokens, 100-200 token overlap

**Chunking Approach:**
```python
def chunk_markdown(content: str, file_path: str) -> list[dict]:
    """
    Chunk markdown content while preserving context.
    
    Strategy:
    1. Split by sections (## headers)
    2. Further split if section > 1000 tokens
    3. Preserve header hierarchy for each chunk
    4. Add overlap from previous chunk
    """
    chunks = []
    sections = split_by_headers(content)
    
    for section in sections:
        header = extract_header(section)
        section_content = remove_header(section)
        
        # If section is small enough, keep as one chunk
        if count_tokens(section_content) <= 1000:
            chunks.append({
                "content": f"{header}\n\n{section_content}",
                "metadata": {
                    "section_heading": header,
                    "file_path": file_path,
                    "chunk_index": len(chunks)
                }
            })
        else:
            # Split large sections
            sub_chunks = split_by_paragraphs(section_content, max_tokens=800)
            for sub_chunk in sub_chunks:
                chunks.append({
                    "content": f"{header}\n\n{sub_chunk}",
                    "metadata": {
                        "section_heading": header,
                        "file_path": file_path,
                        "chunk_index": len(chunks)
                    }
                })
    
    return add_overlap(chunks, overlap_tokens=150)

def add_overlap(chunks: list[dict], overlap_tokens: int) -> list[dict]:
    """Add text from previous chunk for context continuity."""
    for i in range(1, len(chunks)):
        prev_text = chunks[i-1]["content"]
        overlap_text = get_last_n_tokens(prev_text, overlap_tokens)
        chunks[i]["content"] = f"{overlap_text}\n\n---\n\n{chunks[i]['content']}"
    
    return chunks
```

**Special Handling:**

**Code Blocks:**
```python
# Keep code blocks intact (don't split mid-code)
def is_code_block_boundary(text: str, position: int) -> bool:
    lines_before = text[:position].split('\n')
    code_fence_count = sum(1 for line in lines_before if line.strip().startswith('```'))
    return code_fence_count % 2 == 0  # Even count = outside code block
```

**Tables:**
```python
# Keep tables intact
def preserve_tables(text: str) -> list[str]:
    # Detect table boundaries (consecutive lines with |)
    # Split around tables, not through them
    pass
```

**Images:**
```python
# Keep image references with surrounding context
# Don't split immediately before/after image
def preserve_image_context(text: str) -> list[str]:
    # Markdown images: ![alt](url)
    # Keep 1-2 sentences before and after
    pass
```

**Section Headers:**
- Always include section header in chunk
- Include parent headers for context (e.g., "Chapter 3: ROS2 > 3.2 Topics")
- Enables better citations ("Chapter 3, Section 3.2")

**Token Counting:**
```python
import tiktoken

def count_tokens(text: str) -> int:
    """Count tokens using tiktoken (OpenAI's tokenizer, good approximation)."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))
```

**Chunk Size Rationale:**
- **500-1000 tokens**: Balances context richness with retrieval precision
- **Smaller chunks (200-300)**: Too granular, lose context
- **Larger chunks (1500+)**: Dilute semantic focus, harder to cite precisely
- **100-200 token overlap**: Prevents context loss at chunk boundaries

**Expected Chunk Count:**
- 16 chapters × ~2,500 words/chapter = 40,000 words total
- ~50,000 tokens total (assuming 1.25 tokens/word)
- 50,000 / 750 (avg chunk size) = ~67 chunks minimum
- With overlap and splitting: ~200-300 chunks

---

## R5: FastAPI + WebSocket Patterns

### Decision: FastAPI with async endpoints, optional WebSocket for real-time

**FastAPI Application Structure:**
```python
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="RAG Chatbot API",
    description="Backend API for Physical AI & Humanoid Robotics chatbot",
    version="1.0.0"
)

# CORS configuration for Docusaurus
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**REST Endpoint Pattern:**
```python
class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    answer: str
    citations: list[dict]
    session_id: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process chat question and return answer with citations.
    """
    try:
        # Run agent
        result = await run_agent(request.question)
        
        return ChatResponse(
            answer=result["answer"],
            citations=result["citations"],
            session_id=request.session_id or generate_session_id()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "rag-chatbot"}
```

**Async Patterns:**
```python
import asyncio

async def run_agent(question: str) -> dict:
    """
    Orchestrate agent execution asynchronously.
    """
    # Generate query embedding (I/O bound - can be async)
    query_embedding = await asyncio.to_thread(
        generate_query_embedding, question
    )
    
    # Search vector database (I/O bound - can be async)
    chunks = await asyncio.to_thread(
        search_similar_chunks, query_embedding, top_k=5
    )
    
    # Generate response using agent (I/O bound - can be async)
    response = await asyncio.to_thread(
        agent.generate, question, context=chunks
    )
    
    return {
        "answer": response.text,
        "citations": format_citations(chunks)
    }
```

**Error Handling Middleware:**
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if app.debug else "An error occurred",
            "type": type(exc).__name__
        }
    )
```

**WebSocket Pattern (Optional for v1):**
```python
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive question
            data = await websocket.receive_json()
            question = data.get("question")
            
            # Send typing indicator
            await websocket.send_json({"typing": True})
            
            # Process question
            result = await run_agent(question)
            
            # Send response
            await websocket.send_json({
                "answer": result["answer"],
                "citations": result["citations"],
                "typing": False
            })
    except Exception as e:
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()
```

**Logging Configuration:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("rag-chatbot")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
```

**Rationale:**
- **FastAPI**: Modern, async-first, automatic OpenAPI docs, type hints
- **Async/await**: Efficient I/O handling for API calls (Gemini, ChromaDB)
- **CORS**: Essential for frontend-backend communication
- **Pydantic**: Request/response validation, type safety
- **WebSocket**: Optional enhancement for real-time streaming

**Alternatives Considered:**
- **Flask**: Synchronous by default, less modern
- **Django**: Overkill for API-only backend
- **Express.js**: Would require Node.js backend (Python preferred for AI/ML)

---

## R6: React Chat Widget Best Practices

### Decision: Component-based architecture with framer-motion animations

**Component Architecture:**
```
src/components/ChatWidget/
├── ChatWidget.js           # Container component (state management)
├── ChatWidget.module.css   # Scoped styles
├── MessageList.js          # Presentational (display messages)
├── InputBox.js             # Presentational (user input)
├── TypingIndicator.js      # Presentational (bot typing animation)
└── index.js                # Export barrel
```

**ChatWidget.js (Container):**
```jsx
import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import MessageList from './MessageList';
import InputBox from './InputBox';
import styles from './ChatWidget.module.css';

export default function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    const toggleChat = () => setIsOpen(!isOpen);

    const sendMessage = async (text) => {
        // Add user message
        setMessages(prev => [...prev, { sender: 'user', text, timestamp: Date.now() }]);
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text })
            });

            const data = await response.json();

            // Add bot response
            setMessages(prev => [...prev, {
                sender: 'bot',
                text: data.answer,
                citations: data.citations,
                timestamp: Date.now()
            }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                sender: 'bot',
                text: 'Sorry, I encountered an error. Please try again.',
                timestamp: Date.now()
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            {/* Floating button */}
            <motion.button
                className={styles.floatingButton}
                onClick={toggleChat}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.95 }}
                aria-label="Open chat"
            >
                💬
            </motion.button>

            {/* Chat window */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        className={styles.chatWindow}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 20 }}
                        transition={{ duration: 0.3 }}
                    >
                        <div className={styles.header}>
                            <h3>Book Assistant</h3>
                            <button onClick={toggleChat} aria-label="Close chat">✕</button>
                        </div>
                        <MessageList messages={messages} isLoading={isLoading} />
                        <InputBox onSend={sendMessage} disabled={isLoading} />
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
}
```

**MessageList.js (Presentational):**
```jsx
import React, { useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import styles from './MessageList.module.css';

export default function MessageList({ messages, isLoading }) {
    const messagesEndRef = useRef(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isLoading]);

    return (
        <div className={styles.messageList}>
            {messages.map((msg, index) => (
                <motion.div
                    key={index}
                    className={`${styles.message} ${styles[msg.sender]}`}
                    initial={{ opacity: 0, x: msg.sender === 'user' ? 20 : -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3 }}
                >
                    <p>{msg.text}</p>
                    {msg.citations && (
                        <div className={styles.citations}>
                            <strong>Sources:</strong>
                            {msg.citations.map((cite, i) => (
                                <a key={i} href={cite.file_path}>
                                    {cite.chapter_title}
                                </a>
                            ))}
                        </div>
                    )}
                </motion.div>
            ))}
            {isLoading && <TypingIndicator />}
            <div ref={messagesEndRef} />
        </div>
    );
}
```

**InputBox.js:**
```jsx
import React, { useState } from 'react';
import styles from './InputBox.module.css';

export default function InputBox({ onSend, disabled }) {
    const [input, setInput] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !disabled) {
            onSend(input.trim());
            setInput('');
        }
    };

    return (
        <form className={styles.inputBox} onSubmit={handleSubmit}>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about the book..."
                disabled={disabled}
                maxLength={500}
                aria-label="Chat input"
            />
            <button type="submit" disabled={disabled || !input.trim()}>
                Send
            </button>
        </form>
    );
}
```

**Accessibility Implementation:**
```jsx
// Keyboard navigation
useEffect(() => {
    const handleEscape = (e) => {
        if (e.key === 'Escape' && isOpen) {
            setIsOpen(false);
        }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
}, [isOpen]);

// ARIA labels
<button
    aria-label="Open chat"
    aria-expanded={isOpen}
    aria-controls="chat-window"
>
    💬
</button>

// Focus management
useEffect(() => {
    if (isOpen) {
        document.getElementById('chat-input')?.focus();
    }
}, [isOpen]);
```

**Animation Best Practices:**
```jsx
// Smooth transitions
const containerVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: { opacity: 1, scale: 1, transition: { duration: 0.3 } },
    exit: { opacity: 0, scale: 0.9, transition: { duration: 0.2 } }
};

// Stagger children
const listVariants = {
    visible: {
        transition: { staggerChildren: 0.1 }
    }
};
```

**Rationale:**
- **framer-motion**: Industry-standard for React animations, performant
- **Component separation**: Container/presentational pattern for testability
- **CSS Modules**: Scoped styling prevents conflicts with Docusaurus
- **Accessibility-first**: ARIA labels, keyboard navigation, focus management
- **State management**: Local state sufficient (no Redux needed for simple chat)

**Alternatives Considered:**
- **react-spring**: Similar to framer-motion but less intuitive API
- **CSS transitions**: Less flexible, harder to orchestrate complex animations
- **Global state (Redux/Zustand)**: Overkill for single-component feature

---

## R7: Metadata System Design

### Decision: Two-layer metadata system (Summary + Index)

**Summary Metadata (summary_metadata.json):**
```json
{
  "modules": {
    "module-1-physical-ai": {
      "title": "Physical AI Foundations",
      "order": 1,
      "chapters": [
        {
          "id": "01-introduction",
          "number": 1,
          "title": "Introduction to Physical AI",
          "file_path": "docs/module-1-physical-ai/01-introduction.md",
          "topics": ["embodied AI", "robotics", "physical intelligence"],
          "word_count": 2500
        },
        {
          "id": "02-sensors",
          "number": 2,
          "title": "Sensors and Perception",
          "file_path": "docs/module-1-physical-ai/02-sensors.md",
          "topics": ["cameras", "lidar", "IMU", "sensor fusion"],
          "word_count": 3200
        }
      ]
    },
    "module-2-ros2": {
      "title": "ROS2 Middleware",
      "order": 2,
      "chapters": [...]
    }
  },
  "stats": {
    "total_modules": 4,
    "total_chapters": 16,
    "total_words": 42000
  }
}
```

**Index Metadata (index_metadata.json):**
```json
{
  "topic_index": {
    "ROS2": {
      "chapters": [
        "module-2-ros2/01-why-middleware.md",
        "module-2-ros2/02-nodes-topics.md",
        "module-2-ros2/03-services-actions.md"
      ],
      "primary_chapter": "module-2-ros2/01-why-middleware.md"
    },
    "Isaac Sim": {
      "chapters": [
        "module-4-isaac/02-isaac-sim-overview.md",
        "module-4-isaac/03-robot-simulation.md"
      ],
      "primary_chapter": "module-4-isaac/02-isaac-sim-overview.md"
    },
    "balance control": {
      "chapters": [
        "module-1-physical-ai/03-actuation.md",
        "module-3-simulation/04-physics-engines.md"
      ],
      "primary_chapter": "module-1-physical-ai/03-actuation.md"
    }
  },
  "keyword_index": {
    "neural network": ["module-1-physical-ai/04-ai-integration.md"],
    "ZMP": ["module-1-physical-ai/03-actuation.md"],
    "gazebo": ["module-3-simulation/01-simulation-intro.md"]
  }
}
```

**Metadata Query Tool Implementation:**
```python
import json

def query_metadata(query_type: str, query_value: str) -> dict:
    """
    Query book metadata for navigation and structure information.
    
    Supported queries:
    - "chapters_in_module": Return all chapters in a module
    - "find_topic": Find where a topic is covered
    - "module_overview": Get module structure
    """
    with open("backend/vectordb/summary_metadata.json") as f:
        summary = json.load(f)
    
    with open("backend/vectordb/index_metadata.json") as f:
        index = json.load(f)
    
    if query_type == "chapters_in_module":
        module = summary["modules"].get(query_value, {})
        return {
            "module_title": module.get("title"),
            "chapters": [
                {"number": ch["number"], "title": ch["title"]}
                for ch in module.get("chapters", [])
            ]
        }
    
    elif query_type == "find_topic":
        topic_data = index["topic_index"].get(query_value.lower(), {})
        return {
            "topic": query_value,
            "found": bool(topic_data),
            "chapters": topic_data.get("chapters", []),
            "primary_source": topic_data.get("primary_chapter")
        }
    
    elif query_type == "module_overview":
        return {
            "modules": [
                {
                    "name": mod_key,
                    "title": mod_data["title"],
                    "chapter_count": len(mod_data["chapters"])
                }
                for mod_key, mod_data in summary["modules"].items()
            ]
        }
    
    return {"error": "Unknown query type"}
```

**Use Cases:**
1. **"What chapters are in module 2?"**
   - Query: `query_metadata("chapters_in_module", "module-2-ros2")`
   - Response: List of 4 chapters with titles

2. **"Where can I find information about Isaac Sim?"**
   - Query: `query_metadata("find_topic", "Isaac Sim")`
   - Response: Primary chapter + related chapters

3. **"What topics are covered in Chapter 3?"**
   - Load summary metadata, find chapter 3, return topics list

**Rationale:**
- **Two-layer design**: Summary for structure, Index for content discovery
- **JSON format**: Easy to generate, human-readable, no database needed
- **Generated at build time**: Updated when content changes
- **Fast lookups**: In-memory JSON, no API calls needed

---

## Implementation Timeline Summary

Based on research findings:

- **Phase 0 (Research)**: ✅ Complete
- **Phase 1 (Frontend)**: 3-4 hours (audit, cleanup, configuration)
- **Phase 2 (Vector DB)**: 8-10 hours (chunking, embeddings, ChromaDB, metadata)
- **Phase 3 (Agent)**: 8-10 hours (tools, agent setup, testing)
- **Phase 4 (Backend)**: 6-8 hours (FastAPI, endpoints, integration)
- **Phase 5 (Chat Widget)**: 8-10 hours (React components, animations, integration)
- **Phase 6 (Testing)**: 6-8 hours (unit, integration, E2E tests)
- **Phase 7 (Documentation)**: 3-4 hours (setup guide, API docs, deployment)

**Total Estimated Time**: 42-54 hours (5-7 days full-time)

---

## Key Decisions Summary

1. **ADK Agent Pattern**: LlmAgent with modular tools (search, citation, metadata)
2. **Gemini Integration**: text-embedding-004 + gemini-2.0-flash-exp
3. **ChromaDB**: Local persistent storage, no cloud dependencies
4. **Chunking**: 500-1000 tokens with 100-200 overlap, semantic boundaries
5. **FastAPI**: Async REST API with optional WebSocket
6. **React Widget**: framer-motion animations, CSS Modules, accessibility-first
7. **Metadata**: Two-layer system (summary + index) for navigation queries

---

## Next Steps

1. ✅ Research complete - proceed to Phase 1 (Frontend Audit)
2. Update tasks.md to mark research tasks as complete
3. Begin frontend audit and cleanup
4. Create backend directory structure
5. Implement chunking and embedding pipeline
