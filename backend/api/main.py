"""FastAPI main application with CORS and middleware"""

import os
import sys
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.runner import AgentRunner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Global agent runner instance
agent_runner: Optional[AgentRunner] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - load agent on startup"""
    global agent_runner
    
    logger.info("Starting FastAPI application...")
    
    # Load agent on startup
    try:
        logger.info("Initializing AgentRunner...")
        agent_runner = AgentRunner()
        logger.info("✅ AgentRunner initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize AgentRunner: {e}")
        raise
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down FastAPI application...")
    agent_runner = None


# Create FastAPI app with lifespan
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI & Robotics book",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS",'https://basit796.github.io/book_with_rag_agent_with_speckitPlus_live/').split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    """Log all requests and responses"""
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e)
            }
        )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "RAG Chatbot API",
        "version": "1.0.0",
        "status": "running"
    }


# Import routes after app creation to avoid circular imports
from api import routes

# Include API routes
app.include_router(routes.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
