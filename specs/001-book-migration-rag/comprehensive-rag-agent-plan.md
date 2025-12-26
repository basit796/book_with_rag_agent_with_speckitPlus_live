# Comprehensive RAG Agent Implementation Plan

**Feature**: Book Migration & RAG Agent Integration  
**Branch**: `001-book-migration-rag`  
**Created**: 2025-12-25  
**Status**: Planning Phase

---

## Executive Summary

This plan provides a complete roadmap for:
1. Completing the Docusaurus frontend for the Physical AI & Robotics book
2. Creating a vector database with embeddings from book content
3. Building an ADK-compliant agent for intelligent book Q&A
4. Integrating the agent with the frontend via a beautiful, animated chat interface

---

## Phase 1: Frontend Assessment & Completion

### 1.1 Current State Analysis

**Findings from inspection:**
- ✅ Docusaurus is properly configured and runs successfully
- ✅ Dependencies are installed (`node_modules` exists)
- ✅ Book content exists in organized modules:
  - Module 1: Physical AI (4 chapters)
  - Module 2: ROS2 (4 chapters)
  - Module 3: Simulation (4 chapters)
  - Module 4: Isaac (4 chapters)
- ✅ Navigation structure uses auto-generated sidebars
- ⚠️ Configuration still uses default template values (needs customization)
- ⚠️ Default tutorial content still present (needs cleanup)

### 1.2 Frontend Completion Tasks

#### Task 1.2.1: Update Site Configuration
**File**: `Future Ai And Robotics/docusaurus.config.js`
**Changes**:
- Update `title` to "Future AI and Robotics"
- Update `tagline` to relevant book tagline
- Update `url` to actual deployment URL
- Update organization name and project name
- Customize navbar items to reflect book structure
- Update footer with proper links and copyright

#### Task 1.2.2: Clean Up Default Content
**Actions**:
- Remove or customize default tutorial content in `/blog`
- Update `intro.md` to be book-specific introduction
- Remove tutorial-basics and tutorial-extras if not needed
- Ensure all module content is properly linked

#### Task 1.2.3: Enhance Sidebar Navigation
**File**: `Future Ai And Robotics/sidebars.js`
**Changes**:
- Create custom sidebar structure for better book navigation
- Add module categories with descriptions
- Ensure logical chapter ordering

#### Task 1.2.4: Add Custom Styling
**File**: `Future Ai And Robotics/src/css/custom.css`
**Changes**:
- Add custom color scheme matching AI/Robotics theme
- Improve typography for readability
- Add custom styles for code blocks and diagrams
- Prepare CSS for chat widget integration

#### Task 1.2.5: Create Landing Page
**File**: `Future Ai And Robotics/src/pages/index.js`
**Changes**:
- Design attractive landing page for the book
- Add hero section with book overview
- Include module cards with navigation
- Add call-to-action buttons

**Completion Criteria**:
- [ ] All configuration updated with correct information
- [ ] Default content removed or customized
- [ ] Navigation is intuitive and complete
- [ ] Site builds without errors
- [ ] Site is visually appealing and professional

---

## Phase 2: Vector Database & Embeddings

### 2.1 Technology Stack Decision

**Chosen Technologies**:
- **Embedding Model**: Google Gemini (`text-embedding-004`)
- **Vector Store**: ChromaDB (easy setup, persistent storage)
- **Chunking Strategy**: Recursive character text splitter with semantic awareness
- **Backend**: Python FastAPI (better ML library support)

**Rationale**:
- Gemini API provides excellent embeddings at competitive cost
- ChromaDB is lightweight, persistent, and Python-native
- FastAPI offers async support and automatic API documentation
- Python ecosystem has mature RAG libraries

### 2.2 Data Preparation

#### Task 2.2.1: Content Collection Script
**File**: `backend/scripts/collect_content.py`
**Purpose**: Gather all markdown files from docs directory

```python
# Pseudo-structure
def collect_markdown_files(docs_dir):
    """
    Recursively collect all .md files
    Exclude: tutorial-basics, tutorial-extras (if not needed)
    Include: All module-* directories
    """
    pass

def extract_metadata(file_path):
    """
    Extract frontmatter (title, sidebar_position)
    Parse markdown structure (headings)
    """
    pass
```

#### Task 2.2.2: Content Chunking
**File**: `backend/embeddings/chunker.py`
**Strategy**:
- **Chunk Size**: 800 tokens (~600-1000 words)
- **Overlap**: 150 tokens (maintain context)
- **Semantic Boundaries**: Split on headers, paragraphs
- **Metadata Preservation**: Keep chapter, module, heading context

```python
# Pseudo-structure
class DocumentChunker:
    def __init__(self, chunk_size=800, overlap=150):
        pass
    
    def chunk_by_headers(self, content, metadata):
        """
        Split on markdown headers first
        Then apply size limits
        Preserve hierarchy in metadata
        """
        pass
    
    def create_chunk_metadata(self, chunk, source_file, heading_path):
        """
        Returns: {
            'source': 'module-1-physical-ai/01-what-is-physical-ai.md',
            'module': 'Physical AI',
            'chapter': '01',
            'heading': 'What is Physical AI > Definition',
            'chunk_index': 0
        }
        """
        pass
```

#### Task 2.2.3: Embedding Generation
**File**: `backend/embeddings/generator.py`
**Process**:
1. Initialize Gemini API client
2. Batch process chunks (50-100 at a time)
3. Handle rate limits and retries
4. Store embeddings with metadata

```python
# Pseudo-structure
class EmbeddingGenerator:
    def __init__(self, api_key, model="text-embedding-004"):
        pass
    
    async def generate_embeddings(self, texts: List[str]):
        """
        Batch generate embeddings
        Handle API errors and rate limits
        """
        pass
    
    async def embed_document_chunks(self, chunks):
        """
        Process all chunks with metadata
        Return ready-to-store format
        """
        pass
```

#### Task 2.2.4: Vector Store Setup
**File**: `backend/embeddings/vector_store.py`
**Implementation**:

```python
# Pseudo-structure
import chromadb
from chromadb.config import Settings

class BookVectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="book_chapters",
            metadata={"description": "Physical AI & Robotics Book"}
        )
    
    def add_chunks(self, chunks, embeddings, metadatas):
        """
        Add documents to collection
        chunks: List[str] - text content
        embeddings: List[List[float]] - vectors
        metadatas: List[dict] - chunk metadata
        """
        pass
    
    def query(self, query_embedding, n_results=5, filter=None):
        """
        Retrieve most similar chunks
        Supports metadata filtering
        """
        pass
    
    def rebuild_index(self):
        """
        Clear and rebuild entire vector store
        Use when content is updated
        """
        pass
```

### 2.3 Complete Pipeline Script

**File**: `backend/scripts/build_vector_db.py`
**Purpose**: End-to-end pipeline execution

```python
# Pseudo-structure
async def main():
    # 1. Collect all markdown files
    docs = collect_markdown_files("../Future Ai And Robotics/docs")
    
    # 2. Chunk documents
    chunker = DocumentChunker()
    chunks = []
    for doc in docs:
        doc_chunks = chunker.chunk_by_headers(doc.content, doc.metadata)
        chunks.extend(doc_chunks)
    
    # 3. Generate embeddings
    generator = EmbeddingGenerator(api_key=os.getenv("GEMINI_API_KEY"))
    embeddings = await generator.embed_document_chunks(chunks)
    
    # 4. Store in vector DB
    vector_store = BookVectorStore()
    vector_store.add_chunks(
        chunks=[c.text for c in chunks],
        embeddings=embeddings,
        metadatas=[c.metadata for c in chunks]
    )
    
    print(f"✅ Indexed {len(chunks)} chunks from {len(docs)} documents")
```

**Completion Criteria**:
- [ ] All book content successfully chunked
- [ ] Embeddings generated for all chunks
- [ ] Vector store created and queryable
- [ ] Metadata correctly preserved
- [ ] Rebuild script documented and tested

---

## Phase 3: ADK Agent Implementation

### 3.1 ADK Architecture Research

**Research Tasks**:
1. Review Google ADK documentation
2. Understand agent patterns and best practices
3. Identify tool creation patterns
4. Study agent-tool communication protocols

**Key ADK Concepts** (to be researched):
- Agent lifecycle and state management
- Tool definition and registration
- Message passing and context handling
- Error handling and recovery
- Streaming responses

### 3.2 Agent Architecture

**Directory Structure**:
```
backend/
├── agent/
│   ├── __init__.py
│   ├── book_agent.py          # Main agent implementation
│   ├── config.py               # Agent configuration
│   └── prompts.py              # System prompts
├── tools/
│   ├── __init__.py
│   ├── base.py                 # Base tool class
│   ├── search_tool.py          # Vector search tool
│   ├── citation_tool.py        # Citation formatter
│   └── context_tool.py         # Context retrieval
├── runner/
│   ├── __init__.py
│   ├── agent_runner.py         # Agent execution engine
│   └── session_manager.py      # Session handling
└── api/
    ├── __init__.py
    └── routes.py               # FastAPI endpoints
```

### 3.3 Tool Implementations

#### Tool 3.3.1: Search Tool
**File**: `backend/tools/search_tool.py`
**Purpose**: Query vector database for relevant content

```python
# Pseudo-structure
from typing import List, Dict
from pydantic import BaseModel

class SearchToolInput(BaseModel):
    query: str
    num_results: int = 5
    module_filter: Optional[str] = None

class SearchToolOutput(BaseModel):
    chunks: List[Dict]  # text, metadata, similarity_score
    total_found: int

class SearchTool:
    """
    Searches the book content vector database
    for chunks relevant to the user's question
    """
    
    name = "search_book_content"
    description = """
    Search the Physical AI & Robotics book for relevant content.
    Use this when you need to find information to answer user questions.
    """
    
    def __init__(self, vector_store: BookVectorStore):
        self.vector_store = vector_store
        self.embedder = EmbeddingGenerator()
    
    async def execute(self, input: SearchToolInput) -> SearchToolOutput:
        # 1. Generate query embedding
        query_embedding = await self.embedder.generate_embeddings([input.query])
        
        # 2. Search vector store
        results = self.vector_store.query(
            query_embedding=query_embedding[0],
            n_results=input.num_results,
            filter={"module": input.module_filter} if input.module_filter else None
        )
        
        # 3. Format results
        return SearchToolOutput(
            chunks=results,
            total_found=len(results)
        )
```

#### Tool 3.3.2: Citation Formatter
**File**: `backend/tools/citation_tool.py`
**Purpose**: Format sources into proper citations

```python
# Pseudo-structure
class CitationToolInput(BaseModel):
    chunks: List[Dict]  # From search results

class CitationToolOutput(BaseModel):
    formatted_citations: List[str]
    source_links: List[Dict]

class CitationTool:
    """
    Formats search results into proper citations
    with links back to source chapters
    """
    
    name = "format_citations"
    description = """
    Format retrieved chunks into proper citations.
    Use after searching to create source references.
    """
    
    async def execute(self, input: CitationToolInput) -> CitationToolOutput:
        citations = []
        links = []
        
        for chunk in input.chunks:
            metadata = chunk['metadata']
            citation = f"[{metadata['module']}, Chapter {metadata['chapter']}]"
            link = {
                'text': citation,
                'url': f"/docs/{metadata['source'].replace('.md', '')}"
            }
            citations.append(citation)
            links.append(link)
        
        return CitationToolOutput(
            formatted_citations=citations,
            source_links=links
        )
```

### 3.4 Agent Implementation

**File**: `backend/agent/book_agent.py`
**Core Implementation**:

```python
# Pseudo-structure
from typing import List
import google.generativeai as genai

class BookAgent:
    """
    ADK-compliant agent for answering questions about
    the Physical AI & Robotics book using RAG
    """
    
    def __init__(
        self,
        vector_store: BookVectorStore,
        model_name: str = "gemini-2.0-flash-exp",
        tools: List = None
    ):
        self.vector_store = vector_store
        self.model = genai.GenerativeModel(model_name)
        
        # Initialize tools
        self.search_tool = SearchTool(vector_store)
        self.citation_tool = CitationTool()
        self.tools = tools or [self.search_tool, self.citation_tool]
        
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        return """
        You are an expert assistant for the Physical AI & Robotics book.
        Your role is to help readers understand concepts from the book by:
        
        1. Searching the book content for relevant information
        2. Providing accurate, well-cited answers
        3. Being honest when information is not in the book
        4. Encouraging deeper learning with follow-up questions
        
        IMPORTANT:
        - Always use the search_book_content tool to find information
        - Never make up information not in the book
        - Always provide citations with format_citations tool
        - If unsure, say so and suggest related topics from the book
        """
    
    async def process_query(self, user_query: str) -> Dict:
        """
        Main entry point for processing user questions
        
        Returns:
        {
            'answer': str,
            'sources': List[Dict],
            'follow_up_questions': List[str]
        }
        """
        try:
            # 1. Search for relevant content
            search_result = await self.search_tool.execute(
                SearchToolInput(query=user_query, num_results=5)
            )
            
            # 2. Format context for LLM
            context = self._format_context(search_result.chunks)
            
            # 3. Generate response
            prompt = f"""
            User Question: {user_query}
            
            Relevant Book Content:
            {context}
            
            Provide a clear, accurate answer based on the content above.
            Include specific references to which sections you used.
            """
            
            response = await self.model.generate_content_async(
                contents=[self.system_prompt, prompt]
            )
            
            # 4. Format citations
            citations = await self.citation_tool.execute(
                CitationToolInput(chunks=search_result.chunks)
            )
            
            # 5. Generate follow-up questions
            follow_ups = self._generate_follow_ups(user_query, search_result.chunks)
            
            return {
                'answer': response.text,
                'sources': citations.source_links,
                'follow_up_questions': follow_ups,
                'confidence': self._calculate_confidence(search_result.chunks)
            }
            
        except Exception as e:
            return self._handle_error(e)
    
    def _format_context(self, chunks: List[Dict]) -> str:
        """Format retrieved chunks into readable context"""
        context_parts = []
        for i, chunk in enumerate(chunks):
            meta = chunk['metadata']
            context_parts.append(
                f"[Source {i+1}: {meta['module']}, Chapter {meta['chapter']}]\n"
                f"{chunk['text']}\n"
            )
        return "\n---\n".join(context_parts)
    
    def _calculate_confidence(self, chunks: List[Dict]) -> str:
        """Determine confidence based on similarity scores"""
        if not chunks:
            return "low"
        
        avg_score = sum(c.get('similarity', 0) for c in chunks) / len(chunks)
        
        if avg_score > 0.8:
            return "high"
        elif avg_score > 0.6:
            return "medium"
        else:
            return "low"
    
    def _generate_follow_ups(self, query: str, chunks: List[Dict]) -> List[str]:
        """Generate relevant follow-up questions"""
        # Could use LLM to generate these or use template-based approach
        return [
            "Would you like more details on this topic?",
            "Should I explain the related concepts?",
            "Are there specific examples you'd like to explore?"
        ]
    
    def _handle_error(self, error: Exception) -> Dict:
        """Graceful error handling"""
        return {
            'answer': "I encountered an error processing your question. Please try again.",
            'sources': [],
            'follow_up_questions': [],
            'confidence': 'error',
            'error': str(error)
        }
```

### 3.5 Agent Runner

**File**: `backend/runner/agent_runner.py`
**Purpose**: Orchestrate agent execution with session management

```python
# Pseudo-structure
from typing import Dict, Optional
import uuid

class AgentSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history = []
        self.created_at = datetime.now()
    
    def add_interaction(self, query: str, response: Dict):
        self.history.append({
            'timestamp': datetime.now(),
            'query': query,
            'response': response
        })

class AgentRunner:
    """
    Manages agent lifecycle and session state
    """
    
    def __init__(self, agent: BookAgent):
        self.agent = agent
        self.sessions: Dict[str, AgentSession] = {}
    
    def create_session(self) -> str:
        """Create new session and return ID"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = AgentSession(session_id)
        return session_id
    
    async def run(
        self,
        query: str,
        session_id: Optional[str] = None
    ) -> Dict:
        """
        Execute agent with query
        Manage session state
        """
        # Get or create session
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
        else:
            session_id = self.create_session()
            session = self.sessions[session_id]
        
        # Process query
        response = await self.agent.process_query(query)
        
        # Update session
        session.add_interaction(query, response)
        
        # Add session ID to response
        response['session_id'] = session_id
        
        return response
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        """Retrieve conversation history"""
        if session_id in self.sessions:
            return self.sessions[session_id].history
        return []
    
    def cleanup_old_sessions(self, max_age_hours: int = 24):
        """Remove expired sessions"""
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        expired = [
            sid for sid, session in self.sessions.items()
            if session.created_at < cutoff
        ]
        for sid in expired:
            del self.sessions[sid]
```

**Completion Criteria**:
- [ ] All tools implemented and tested
- [ ] Agent successfully answers book questions
- [ ] Citations correctly formatted
- [ ] Error handling robust
- [ ] Session management working

---

## Phase 4: FastAPI Backend

### 4.1 API Structure

**File**: `backend/api/routes.py`
**Endpoints**:

```python
# Pseudo-structure
from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Book RAG Agent API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Docusaurus dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent runner instance
agent_runner: Optional[AgentRunner] = None

@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    global agent_runner
    
    # Load vector store
    vector_store = BookVectorStore()
    
    # Create agent
    agent = BookAgent(vector_store)
    
    # Create runner
    agent_runner = AgentRunner(agent)
    
    print("✅ Agent initialized and ready")

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict]
    follow_up_questions: List[str]
    confidence: str
    session_id: str

@app.post("/api/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Main endpoint for asking questions
    """
    if not agent_runner:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        response = await agent_runner.run(
            query=request.query,
            session_id=request.session_id
        )
        return QueryResponse(**response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}/history")
async def get_history(session_id: str):
    """
    Retrieve conversation history
    """
    if not agent_runner:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    history = agent_runner.get_session_history(session_id)
    return {"history": history}

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "agent_ready": agent_runner is not None
    }

@app.post("/api/rebuild-index")
async def rebuild_index():
    """
    Trigger vector database rebuild
    (Should be protected with authentication in production)
    """
    try:
        # Run rebuild script
        subprocess.run(
            ["python", "scripts/build_vector_db.py"],
            check=True
        )
        return {"status": "success", "message": "Index rebuilt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: WebSocket for streaming responses
@app.websocket("/ws/query")
async def websocket_query(websocket: WebSocket):
    """
    WebSocket endpoint for streaming responses
    """
    await websocket.accept()
    
    try:
        while True:
            # Receive query
            data = await websocket.receive_json()
            query = data.get("query")
            
            # Process and stream response
            async for chunk in agent_runner.stream_response(query):
                await websocket.send_json({"chunk": chunk})
            
            await websocket.send_json({"done": True})
    
    except Exception as e:
        await websocket.close(code=1011, reason=str(e))
```

### 4.2 Configuration

**File**: `backend/config.py`

```python
# Pseudo-structure
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str
    
    # Vector Store
    chroma_persist_directory: str = "./chroma_db"
    
    # Agent Configuration
    agent_model: str = "gemini-2.0-flash-exp"
    max_search_results: int = 5
    chunk_size: int = 800
    chunk_overlap: int = 150
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Session Management
    session_max_age_hours: int = 24
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

**File**: `backend/.env.example`
```bash
GEMINI_API_KEY=your_api_key_here
CHROMA_PERSIST_DIRECTORY=./chroma_db
AGENT_MODEL=gemini-2.0-flash-exp
API_HOST=0.0.0.0
API_PORT=8000
```

### 4.3 Dependencies

**File**: `backend/requirements.txt`
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
chromadb==0.4.22
google-generativeai==0.3.2
python-markdown==3.5.1
aiofiles==23.2.1
python-dotenv==1.0.0
```

**Completion Criteria**:
- [ ] All API endpoints implemented
- [ ] CORS configured correctly
- [ ] Error handling comprehensive
- [ ] Health checks working
- [ ] Documentation auto-generated (FastAPI Swagger)

---

## Phase 5: Frontend Integration

### 5.1 Chat Widget Component

**File**: `Future Ai And Robotics/src/components/ChatWidget/index.js`

```jsx
// Pseudo-structure
import React, { useState, useEffect, useRef } from 'react';
import './styles.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage = {
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call API
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          session_id: sessionId
        })
      });

      const data = await response.json();

      // Update session ID
      if (data.session_id) {
        setSessionId(data.session_id);
      }

      // Add bot response
      const botMessage = {
        type: 'bot',
        content: data.answer,
        sources: data.sources,
        followUps: data.follow_up_questions,
        confidence: data.confidence,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      // Handle error
      const errorMessage = {
        type: 'error',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-widget-container">
      {/* Floating Button */}
      {!isOpen && (
        <button 
          className="chat-toggle-button"
          onClick={toggleChat}
          aria-label="Open chat"
        >
          <svg>{ /* Chat icon SVG */ }</svg>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className={`chat-window ${isOpen ? 'open' : ''}`}>
          {/* Header */}
          <div className="chat-header">
            <h3>Book Assistant</h3>
            <button 
              className="close-button"
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.length === 0 && (
              <div className="welcome-message">
                👋 Hi! Ask me anything about the Physical AI & Robotics book!
              </div>
            )}
            
            {messages.map((msg, index) => (
              <Message key={index} message={msg} />
            ))}
            
            {isLoading && <LoadingIndicator />}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="chat-input-container">
            <textarea
              className="chat-input"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question..."
              rows="2"
              disabled={isLoading}
            />
            <button
              className="send-button"
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const Message = ({ message }) => {
  return (
    <div className={`message message-${message.type}`}>
      <div className="message-content">
        {message.content}
      </div>
      
      {message.sources && message.sources.length > 0 && (
        <div className="message-sources">
          <strong>Sources:</strong>
          {message.sources.map((source, idx) => (
            <a key={idx} href={source.url} className="source-link">
              {source.text}
            </a>
          ))}
        </div>
      )}
      
      {message.followUps && message.followUps.length > 0 && (
        <div className="follow-up-questions">
          <strong>Follow-up questions:</strong>
          {message.followUps.map((q, idx) => (
            <button key={idx} className="follow-up-button">
              {q}
            </button>
          ))}
        </div>
      )}
      
      <div className="message-timestamp">
        {message.timestamp.toLocaleTimeString()}
      </div>
    </div>
  );
};

const LoadingIndicator = () => {
  return (
    <div className="loading-indicator">
      <div className="typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
};

export default ChatWidget;
```

### 5.2 Chat Widget Styles

**File**: `Future Ai And Robotics/src/components/ChatWidget/styles.css`

```css
/* Pseudo-structure */
.chat-widget-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Toggle Button */
.chat-toggle-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-toggle-button:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.chat-toggle-button svg {
  width: 28px;
  height: 28px;
  fill: white;
}

/* Chat Window */
.chat-window {
  width: 380px;
  height: 600px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  animation: slideUp 0.3s ease-out;
  overflow: hidden;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Header */
.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 28px;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background 0.2s;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Messages Container */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f7f7f8;
}

.welcome-message {
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 14px;
}

/* Message */
.message {
  margin-bottom: 16px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message-user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 12px 16px;
  border-radius: 18px 18px 4px 18px;
  display: inline-block;
  max-width: 80%;
  word-wrap: break-word;
  margin-left: auto;
  float: right;
  clear: both;
}

.message-bot .message-content {
  background: white;
  color: #333;
  padding: 12px 16px;
  border-radius: 18px 18px 18px 4px;
  display: inline-block;
  max-width: 80%;
  word-wrap: break-word;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.message-error .message-content {
  background: #fee;
  color: #c33;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 3px solid #c33;
}

/* Sources */
.message-sources {
  margin-top: 8px;
  font-size: 12px;
  color: #666;
}

.source-link {
  display: inline-block;
  margin: 4px 8px 4px 0;
  padding: 4px 8px;
  background: #f0f0f0;
  border-radius: 4px;
  text-decoration: none;
  color: #667eea;
  transition: background 0.2s;
}

.source-link:hover {
  background: #e0e0e0;
}

/* Follow-up Questions */
.follow-up-questions {
  margin-top: 8px;
}

.follow-up-button {
  display: block;
  margin: 4px 0;
  padding: 8px 12px;
  background: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 6px;
  text-align: left;
  cursor: pointer;
  font-size: 13px;
  color: #555;
  transition: all 0.2s;
  width: 100%;
}

.follow-up-button:hover {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

/* Timestamp */
.message-timestamp {
  font-size: 11px;
  color: #999;
  margin-top: 4px;
}

/* Loading Indicator */
.loading-indicator {
  display: flex;
  align-items: center;
  padding: 12px 16px;
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.7;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* Input Container */
.chat-input-container {
  padding: 16px;
  background: white;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 8px;
}

.chat-input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 14px;
  resize: none;
  font-family: inherit;
  transition: border-color 0.2s;
}

.chat-input:focus {
  outline: none;
  border-color: #667eea;
}

.chat-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.send-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.send-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 480px) {
  .chat-window {
    width: 100vw;
    height: 100vh;
    border-radius: 0;
    bottom: 0;
    right: 0;
  }
  
  .chat-widget-container {
    bottom: 0;
    right: 0;
  }
}
```

### 5.3 Integration with Docusaurus

**File**: `Future Ai And Robotics/src/theme/Root.js`

```jsx
import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

// Wrap the entire app to add chat widget
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
```

**Completion Criteria**:
- [ ] Chat widget renders on all pages
- [ ] Open/close animations smooth
- [ ] Messages display correctly
- [ ] Loading states clear
- [ ] Responsive on mobile
- [ ] Accessible via keyboard

---

## Phase 6: Testing & Validation

### 6.1 Backend Tests

**File**: `backend/tests/test_agent.py`

```python
import pytest
from backend.agent.book_agent import BookAgent
from backend.embeddings.vector_store import BookVectorStore

@pytest.fixture
async def agent():
    vector_store = BookVectorStore()
    return BookAgent(vector_store)

@pytest.mark.asyncio
async def test_agent_answers_question(agent):
    response = await agent.process_query(
        "What is Physical AI?"
    )
    
    assert response['answer']
    assert len(response['sources']) > 0
    assert response['confidence'] in ['high', 'medium', 'low']

@pytest.mark.asyncio
async def test_agent_handles_unknown_topic(agent):
    response = await agent.process_query(
        "How do I bake a cake?"
    )
    
    assert 'not covered' in response['answer'].lower() or \
           response['confidence'] == 'low'

@pytest.mark.asyncio
async def test_citations_valid(agent):
    response = await agent.process_query(
        "What are humanoid robots?"
    )
    
    for source in response['sources']:
        assert 'url' in source
        assert source['url'].startswith('/docs/')
```

### 6.2 Integration Tests

**File**: `backend/tests/test_api.py`

```python
import pytest
from fastapi.testclient import TestClient
from backend.api.routes import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'

def test_query_endpoint():
    response = client.post(
        "/api/query",
        json={"query": "What is ROS2?"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert 'answer' in data
    assert 'sources' in data
    assert 'session_id' in data

def test_invalid_query():
    response = client.post(
        "/api/query",
        json={"query": ""}
    )
    
    assert response.status_code == 422  # Validation error
```

### 6.3 Frontend Tests

**File**: `Future Ai And Robotics/src/components/ChatWidget/__tests__/index.test.js`

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatWidget from '../index';

describe('ChatWidget', () => {
  test('renders toggle button', () => {
    render(<ChatWidget />);
    const button = screen.getByLabelText('Open chat');
    expect(button).toBeInTheDocument();
  });

  test('opens chat window on click', () => {
    render(<ChatWidget />);
    const button = screen.getByLabelText('Open chat');
    fireEvent.click(button);
    
    expect(screen.getByText('Book Assistant')).toBeInTheDocument();
  });

  test('sends message and displays response', async () => {
    // Mock fetch
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({
          answer: 'Test answer',
          sources: [],
          follow_up_questions: [],
          confidence: 'high',
          session_id: 'test-123'
        })
      })
    );

    render(<ChatWidget />);
    
    // Open chat
    fireEvent.click(screen.getByLabelText('Open chat'));
    
    // Type and send message
    const input = screen.getByPlaceholderText('Ask a question...');
    fireEvent.change(input, { target: { value: 'Test question' } });
    fireEvent.click(screen.getByText('Send'));
    
    // Wait for response
    await waitFor(() => {
      expect(screen.getByText('Test answer')).toBeInTheDocument();
    });
  });
});
```

### 6.4 End-to-End Tests

**Manual Testing Checklist**:

```markdown
## E2E Testing Checklist

### Frontend
- [ ] Chat widget visible on all doc pages
- [ ] Toggle button works smoothly
- [ ] Chat opens with welcome message
- [ ] Message sending works
- [ ] Loading indicator appears
- [ ] Responses display correctly
- [ ] Source links are clickable and navigate correctly
- [ ] Follow-up questions are interactive
- [ ] Chat is responsive on mobile
- [ ] Keyboard navigation works
- [ ] Close button works

### Backend
- [ ] Server starts without errors
- [ ] Health check returns success
- [ ] Query endpoint responds correctly
- [ ] Sessions are maintained across requests
- [ ] Error handling works for invalid queries
- [ ] Citations include correct links
- [ ] Confidence scores are reasonable

### RAG Quality
- [ ] Questions about Physical AI are answered accurately
- [ ] Questions about ROS2 are answered accurately
- [ ] Questions about simulation are answered accurately
- [ ] Questions about Isaac are answered accurately
- [ ] Out-of-scope questions handled gracefully
- [ ] Citations point to correct chapters
- [ ] Multiple related chunks are synthesized
- [ ] Semantic search finds relevant content

### Performance
- [ ] Responses return within 3 seconds
- [ ] Multiple concurrent requests handled
- [ ] No memory leaks after extended use
- [ ] Vector search is fast (<500ms)
- [ ] Frontend remains responsive
```

---

## Phase 7: Deployment & Documentation

### 7.1 Deployment Guide

**File**: `deployment/README.md`

```markdown
# Deployment Guide

## Prerequisites
- Node.js 20+
- Python 3.11+
- Gemini API key

## Backend Deployment

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API key
```

3. Build vector database:
```bash
python scripts/build_vector_db.py
```

4. Start server:
```bash
uvicorn api.routes:app --host 0.0.0.0 --port 8000
```

## Frontend Deployment

1. Install dependencies:
```bash
cd "Future Ai And Robotics"
npm install
```

2. Configure API endpoint:
```bash
# Edit src/components/ChatWidget/index.js
# Update API_URL for production
```

3. Build site:
```bash
npm run build
```

4. Deploy (choose one):
   - Netlify: Connect repo, set build command
   - Vercel: Import project, configure build
   - GitHub Pages: Use docusaurus deploy command
```

### 7.2 User Documentation

**File**: `Future Ai And Robotics/docs/using-chat-assistant.md`

```markdown
# Using the Book Chat Assistant

## Overview
The chat assistant helps you explore and understand the Physical AI & Robotics book by answering questions about the content.

## How to Use

1. **Open the Chat**: Click the chat icon in the bottom-right corner
2. **Ask a Question**: Type your question in natural language
3. **Review the Answer**: Read the response with source citations
4. **Explore Further**: Click on sources or follow-up questions

## Tips for Best Results

- **Be Specific**: Instead of "Tell me about robots," ask "What are the main challenges in humanoid balance control?"
- **Reference Topics**: Mention specific concepts like "ROS2 nodes" or "Isaac Sim"
- **Use Citations**: Click source links to read full context
- **Ask Follow-ups**: Dig deeper into topics that interest you

## What the Assistant Can Do

✅ Answer questions about book content
✅ Provide citations to source chapters
✅ Suggest related topics
✅ Explain complex concepts

❌ Cannot answer questions outside the book
❌ No real-time external information
❌ No code execution or debugging

## Example Questions

- "What is Physical AI and how is it different from traditional AI?"
- "How does ROS2 handle communication between nodes?"
- "Why is simulation important in robotics development?"
- "What are the key features of Isaac Sim?"
```

### 7.3 Developer Documentation

**File**: `backend/README.md`

```markdown
# RAG Agent Backend

## Architecture

```
User Query → FastAPI → Agent Runner → Book Agent
                                      ↓
                                   Search Tool → Vector Store
                                      ↓
                                   LLM (Gemini) → Response
                                      ↓
                                   Citation Tool
```

## Development Setup

[Setup instructions...]

## Adding New Tools

[Tool development guide...]

## Updating the Index

```bash
python scripts/build_vector_db.py
```

## API Reference

[API documentation...]
```

**Completion Criteria**:
- [ ] All deployment steps documented
- [ ] User guide complete
- [ ] Developer documentation written
- [ ] Troubleshooting guide included

---

## Implementation Timeline

### Week 1: Frontend & Preparation
- Days 1-2: Complete frontend updates (Phase 1)
- Days 3-4: Set up backend structure
- Day 5: Research ADK best practices

### Week 2: Data & Embeddings
- Days 1-2: Implement chunking and embedding generation
- Days 3-4: Build vector database
- Day 5: Test search quality

### Week 3: Agent Development
- Days 1-3: Implement agent and tools
- Days 4-5: Build agent runner and session management

### Week 4: API & Integration
- Days 1-2: Build FastAPI backend
- Days 3-5: Integrate chat widget with frontend

### Week 5: Testing & Polish
- Days 1-3: Comprehensive testing
- Days 4-5: Documentation and deployment prep

---

## Success Metrics

### Functional Metrics
- ✅ All 16 chapters indexed with embeddings
- ✅ Agent responds in <3 seconds
- ✅ 95%+ accuracy on test questions
- ✅ Citations link to correct chapters
- ✅ Chat widget works on all browsers

### Quality Metrics
- ✅ User can complete Q&A flow in <30 seconds
- ✅ Answers are coherent and well-sourced
- ✅ UI is smooth and responsive
- ✅ Error messages are helpful

### Technical Metrics
- ✅ API handles 10 concurrent requests
- ✅ No memory leaks after 100 queries
- ✅ Vector search <500ms
- ✅ Frontend bundle <2MB

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Gemini API unavailable | Implement retry logic, cache common queries |
| Poor search quality | Iterate on chunking strategy, test with real questions |
| Slow response times | Optimize vector search, consider caching |
| Frontend performance | Code splitting, lazy loading, optimize bundle |
| Incorrect citations | Add validation layer, test with known Q&A pairs |

---

## Next Steps

1. **Review this plan** - Ensure all requirements are covered
2. **Set up environment** - Install dependencies, get API keys
3. **Start with Phase 1** - Complete frontend first
4. **Iterate and test** - Build incrementally with testing
5. **Document progress** - Update PHRs and maintain history

---

## Questions & Clarifications

### ADK Agent Framework
- Need to research Google ADK documentation
- Confirm best practices for tool creation
- Understand agent lifecycle management

### Deployment
- Confirm target deployment platform
- Determine if backend needs containerization
- Decide on production vector store location

### Content Updates
- Process for regenerating embeddings when book updates
- Version control strategy for vector database
- CI/CD integration for automated rebuilds

---

**Ready to begin implementation!**
