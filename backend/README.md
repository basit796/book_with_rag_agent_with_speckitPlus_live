# RAG Chatbot Backend

FastAPI-based backend for the Physical AI & Humanoid Robotics chatbot with RAG (Retrieval-Augmented Generation) capabilities.

## Features

- 🤖 **Google Gemini Integration**: Uses Gemini 2.0 Flash for intelligent responses
- 🔍 **Vector Search**: FAISS-based semantic search across book content
- 📚 **Citation System**: Automatic citation generation with chapter references
- 🔄 **Session Management**: Conversation tracking with session IDs
- ⚡ **Fast API**: Async FastAPI endpoints with <3s response time
- 🧪 **Comprehensive Tests**: 20+ test cases with mocking

## Prerequisites

- Python 3.9+
- Google Gemini API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Required packages:**
- fastapi==0.115.12
- uvicorn==0.32.1
- google-generativeai==0.8.3
- faiss-cpu==1.9.0.post1
- python-dotenv==1.0.1
- pydantic==2.10.5

### 2. Configure Environment

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_EMBEDDING_MODEL=models/text-embedding-004
GEMINI_GENERATION_MODEL=gemini-2.0-flash-exp
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 3. Build Vector Index (First Time Only)

```bash
cd backend
python vectordb/build_index.py
```

This will:
- Process all 16 book chapters
- Generate embeddings for 93 chunks
- Create FAISS index in `vectordb/vector_db/`
- Generate metadata files

**Expected output:**
```
Processing: docs/module-1-physical-ai/01-introduction.md
Chunks created: 93
Generating embeddings (batch size: 10)...
Embeddings generated: 93
Saving FAISS index...
Index built successfully!
```

## Running the Server

### Development Mode (with auto-reload)

```bash
cd backend
python3 -m uvicorn api.main:app --reload --port 8000
```

### Production Mode

```bash
cd backend
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will start on: **http://localhost:8000**

## API Endpoints

### 1. POST /api/chat

Process a user question and return an AI-generated answer with citations.

**Request:**
```json
{
  "question": "What is physical AI?",
  "session_id": "session_abc123" // Optional
}
```

**Validation:**
- Question length: 10-500 characters
- Non-empty after trimming

**Response:**
```json
{
  "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world...",
  "citations": [
    {
      "module_title": "Physical AI Foundations",
      "chapter_title": "Introduction to Physical AI",
      "file_path": "docs/module-1-physical-ai/01-introduction.md",
      "chunk_text": "Physical AI combines...",
      "similarity_score": 0.89
    }
  ],
  "session_id": "session_abc123",
  "response_time_ms": 2458,
  "timestamp": "2025-12-25T17:30:00Z"
}
```

**Error Responses:**
- `400`: Validation error (too short/long)
- `408`: Request timeout (>30s)
- `500`: Internal server error

### 2. GET /api/health

Health check endpoint with component status.

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "api": "running",
    "agent": "loaded",
    "embeddings": "loaded"
  },
  "timestamp": "2025-12-25T17:30:00Z"
}
```

### 3. GET /api/stats

Database statistics.

**Response:**
```json
{
  "total_chunks": 93,
  "modules": 4,
  "chapters": 16,
  "topics": 35
}
```

## Testing

### Run Unit Tests

```bash
cd backend
pytest api/test_api.py -v
```

**Test Coverage:**
- Root endpoint (/)
- Health check endpoint
- Stats endpoint
- Chat endpoint (success, validation, errors)
- CORS configuration

### Manual Testing

```bash
# Test health check
curl http://localhost:8000/api/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is physical AI?"}'

# Test stats
curl http://localhost:8000/api/stats
```

## Architecture

```
backend/
├── agent/                 # Agent implementation
│   ├── agent.py          # BookAgent class with Gemini
│   ├── tools.py          # RAG tools (search, citation, metadata)
│   └── runner.py         # Agent orchestration
├── api/                  # FastAPI application
│   ├── main.py          # App initialization, CORS, middleware
│   ├── routes.py        # Endpoint definitions
│   └── test_api.py      # API tests
├── vectordb/            # Vector database
│   ├── chunker.py       # Markdown chunking
│   ├── embeddings.py    # Gemini embeddings
│   ├── store_faiss.py   # FAISS operations
│   ├── build_index.py   # Index builder script
│   └── vector_db/       # FAISS index storage
├── requirements.txt     # Python dependencies
└── .env                 # Environment configuration
```

## Data Flow

1. **User Question** → Chat Widget (Frontend)
2. **HTTP POST** → `/api/chat` endpoint
3. **Query Embedding** → Gemini API (text-embedding-004)
4. **Vector Search** → FAISS index (top-5 similar chunks)
5. **Context Assembly** → Combine chunks with metadata
6. **Response Generation** → Gemini API (gemini-2.0-flash-exp)
7. **Citation Formatting** → Extract chapter references
8. **JSON Response** → Return to frontend

## Performance

- **Response Time**: <3 seconds end-to-end
- **Vector Search**: <100ms for similarity search
- **Concurrent Requests**: Supports 10+ simultaneous users
- **Index Size**: ~2MB (93 chunks × 768 dimensions)

## Troubleshooting

### "ModuleNotFoundError: No module named 'google.generativeai'"

Install dependencies:
```bash
pip install -r requirements.txt
```

### "FAISS index not found"

Build the index first:
```bash
python vectordb/build_index.py
```

### "Invalid API key"

Check your `.env` file has the correct `GEMINI_API_KEY`.

### CORS errors

Update `CORS_ORIGINS` in `.env` to include your frontend URL.

### "Rate limit exceeded" (429 error)

You've hit the Gemini API free tier limit. Wait a bit or upgrade your quota.

## Development

### Adding New Tools

1. Create tool function in `agent/tools.py`
2. Add function description
3. Update `BookAgent.tools` list in `agent/agent.py`
4. Test with `agent.query("test question")`

### Updating Index

After modifying book content:
```bash
python vectordb/build_index.py
```

This regenerates embeddings for all chapters.

## Production Deployment

### Environment Variables

Set these in production:
- `GEMINI_API_KEY`: Your production API key
- `CORS_ORIGINS`: Your domain (e.g., `https://yourdomain.com`)
- `LOG_LEVEL`: Set to `WARNING` or `ERROR`

### Scaling

For high traffic:
- Use multiple workers: `--workers 4`
- Enable gunicorn: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.main:app`
- Cache embeddings in Redis
- Use Vertex AI for managed Gemini API

## License

MIT License - See LICENSE file

## Support

For issues or questions, please open an issue on GitHub.
