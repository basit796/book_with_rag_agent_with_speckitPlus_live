"""API routes for chat endpoints"""

import logging
import asyncio
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, validator

# Global import to access agent_runner from main
import api.main as main

logger = logging.getLogger(__name__)

router = APIRouter()


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model"""
    question: str = Field(..., min_length=10, max_length=500, description="User question")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation tracking")
    
    @validator('question')
    def validate_question(cls, v):
        """Validate question is not just whitespace"""
        if not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()


class Citation(BaseModel):
    """Citation model"""
    chapter: str = Field(..., description="Chapter title")
    section: Optional[str] = Field(None, description="Section heading")
    module: Optional[str] = Field(None, description="Module name")


class ChatResponse(BaseModel):
    """Chat response model"""
    answer: str = Field(..., description="Generated answer")
    citations: list[Citation] = Field(default_factory=list, description="Source citations")
    session_id: str = Field(..., description="Session ID")
    response_time_ms: int = Field(..., description="Response time in milliseconds")
    timestamp: str = Field(..., description="Response timestamp")


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Overall status")
    checks: dict = Field(..., description="Individual health checks")
    timestamp: str = Field(..., description="Check timestamp")


class StatsResponse(BaseModel):
    """Statistics response model"""
    total_chunks: int = Field(..., description="Total chunks in vector DB")
    modules: int = Field(..., description="Number of modules")
    chapters: int = Field(..., description="Number of chapters")
    topics: int = Field(..., description="Number of topics")


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, http_request: Request):
    """
    Main chat endpoint - processes user questions with RAG
    
    Args:
        request: ChatRequest containing question and optional session_id
        
    Returns:
        ChatResponse with answer, citations, and metadata
        
    Raises:
        HTTPException: 500 if agent is not initialized
        HTTPException: 504 if request times out
        HTTPException: 400 if question is invalid
    """
    start_time = datetime.now()
    
    # Check if agent is initialized
    if main.agent_runner is None:
        logger.error("Agent runner not initialized")
        raise HTTPException(
            status_code=500,
            detail="Chat service not available - agent not initialized"
        )
    
    logger.info(f"Processing chat request: {request.question[:50]}...")
    
    try:
        # Run agent with timeout
        result = await asyncio.wait_for(
            asyncio.to_thread(
                main.agent_runner.run,
                request.question,
                request.session_id
            ),
            timeout=30.0  # 30 second timeout
        )
        
        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Extract citations from result
        citations = []
        if "citations" in result:
            for cite in result["citations"]:
                citations.append(Citation(
                    chapter=cite.get("chapter", "Unknown"),
                    section=cite.get("section"),
                    module=cite.get("module")
                ))
        
        logger.info(f"✅ Chat response generated in {response_time:.0f}ms")
        
        return ChatResponse(
            answer=result.get("answer", "Unable to generate response"),
            citations=citations,
            session_id=result.get("session_id", request.session_id or "default"),
            response_time_ms=int(response_time),
            timestamp=datetime.now().isoformat()
        )
        
    except asyncio.TimeoutError:
        logger.error("Chat request timed out after 30 seconds")
        raise HTTPException(
            status_code=504,
            detail="Request timed out - please try again with a simpler question"
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_endpoint():
    """
    Health check endpoint
    
    Returns:
        HealthResponse with status of API, agent, and embeddings
    """
    checks = {
        "api_running": True,
        "agent_loaded": main.agent_runner is not None,
        "embeddings_loaded": False
    }
    
    # Check if embeddings are loaded
    if main.agent_runner is not None:
        try:
            # Try to get statistics from agent
            stats = main.agent_runner.get_statistics()
            checks["embeddings_loaded"] = stats.get("total_chunks", 0) > 0
        except Exception as e:
            logger.warning(f"Failed to check embeddings: {e}")
    
    # Determine overall status
    overall_status = "healthy" if all(checks.values()) else "degraded"
    
    return HealthResponse(
        status=overall_status,
        checks=checks,
        timestamp=datetime.now().isoformat()
    )


@router.get("/stats", response_model=StatsResponse)
async def stats_endpoint():
    """
    Statistics endpoint
    
    Returns:
        StatsResponse with database statistics
        
    Raises:
        HTTPException: 500 if agent is not initialized
    """
    if main.agent_runner is None:
        raise HTTPException(
            status_code=500,
            detail="Agent not initialized"
        )
    
    try:
        stats = main.agent_runner.get_statistics()
        
        return StatsResponse(
            total_chunks=stats.get("total_chunks", 0),
            modules=stats.get("modules", 0),
            chapters=stats.get("chapters", 0),
            topics=stats.get("topics", 0)
        )
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )
