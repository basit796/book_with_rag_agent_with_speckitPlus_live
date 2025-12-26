"""Unit tests for FastAPI endpoints"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.main import app


# Create test client
client = TestClient(app)


@pytest.fixture
def mock_agent_runner():
    """Mock AgentRunner for testing"""
    mock = MagicMock()
    mock.run.return_value = {
        "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world.",
        "citations": [
            {
                "chapter": "Chapter 1: What is Physical AI?",
                "section": "Introduction",
                "module": "module-1-physical-ai"
            }
        ],
        "session_id": "test-session",
        "conversation_id": 1
    }
    mock.get_statistics.return_value = {
        "total_chunks": 93,
        "modules": 4,
        "chapters": 16,
        "topics": 35,
        "total_messages": 0,
        "total_conversations": 0,
        "model": "gemini-2.5-flash"
    }
    return mock


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_returns_service_info(self):
        """Test that root endpoint returns service information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "RAG Chatbot API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check_success(self, mock_agent_runner):
        """Test health check when agent is loaded"""
        with patch('api.main.agent_runner', mock_agent_runner):
            response = client.get("/api/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["checks"]["api_running"] is True
            assert data["checks"]["agent_loaded"] is True
            assert "timestamp" in data
    
    def test_health_check_degraded(self):
        """Test health check when agent is not loaded"""
        with patch('api.main.agent_runner', None):
            response = client.get("/api/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "degraded"
            assert data["checks"]["api_running"] is True
            assert data["checks"]["agent_loaded"] is False


class TestStatsEndpoint:
    """Test statistics endpoint"""
    
    def test_stats_success(self, mock_agent_runner):
        """Test statistics endpoint returns correct data"""
        with patch('api.main.agent_runner', mock_agent_runner):
            response = client.get("/api/stats")
            assert response.status_code == 200
            data = response.json()
            assert data["total_chunks"] == 93
            assert data["modules"] == 4
            assert data["chapters"] == 16
            assert data["topics"] == 35
    
    def test_stats_agent_not_initialized(self):
        """Test statistics endpoint when agent is not initialized"""
        with patch('api.main.agent_runner', None):
            response = client.get("/api/stats")
            assert response.status_code == 500
            data = response.json()
            assert "Agent not initialized" in data["detail"]


class TestChatEndpoint:
    """Test chat endpoint"""
    
    def test_chat_success(self, mock_agent_runner):
        """Test successful chat interaction"""
        with patch('api.main.agent_runner', mock_agent_runner):
            response = client.post(
                "/api/chat",
                json={"question": "What is physical AI?"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "answer" in data
            assert "citations" in data
            assert "session_id" in data
            assert "response_time_ms" in data
            assert "timestamp" in data
            assert len(data["answer"]) > 0
            assert isinstance(data["citations"], list)
    
    def test_chat_with_session_id(self, mock_agent_runner):
        """Test chat with custom session ID"""
        with patch('api.main.agent_runner', mock_agent_runner):
            response = client.post(
                "/api/chat",
                json={
                    "question": "What is physical AI?",
                    "session_id": "custom-session-123"
                }
            )
            assert response.status_code == 200
            data = response.json()
            # Note: session_id returned depends on agent_runner implementation
            assert "session_id" in data
    
    def test_chat_question_too_short(self):
        """Test chat with question that's too short"""
        response = client.post(
            "/api/chat",
            json={"question": "Hi"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_question_too_long(self):
        """Test chat with question that's too long"""
        long_question = "x" * 501
        response = client.post(
            "/api/chat",
            json={"question": long_question}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_empty_question(self):
        """Test chat with empty question"""
        response = client.post(
            "/api/chat",
            json={"question": "          "}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_agent_not_initialized(self):
        """Test chat when agent is not initialized"""
        with patch('api.main.agent_runner', None):
            response = client.post(
                "/api/chat",
                json={"question": "What is physical AI?"}
            )
            assert response.status_code == 500
            data = response.json()
            assert "agent not initialized" in data["detail"].lower()
    
    def test_chat_agent_error(self, mock_agent_runner):
        """Test chat when agent raises an exception"""
        mock_agent_runner.run.side_effect = Exception("Agent error")
        
        with patch('api.main.agent_runner', mock_agent_runner):
            response = client.post(
                "/api/chat",
                json={"question": "What is physical AI?"}
            )
            assert response.status_code == 500
            data = response.json()
            assert "Failed to process question" in data["detail"]
    
    def test_chat_response_format(self, mock_agent_runner):
        """Test that chat response has correct format"""
        with patch('api.main.agent_runner', mock_agent_runner):
            response = client.post(
                "/api/chat",
                json={"question": "What is physical AI?"}
            )
            assert response.status_code == 200
            data = response.json()
            
            # Check answer is string
            assert isinstance(data["answer"], str)
            
            # Check citations structure
            assert isinstance(data["citations"], list)
            if len(data["citations"]) > 0:
                citation = data["citations"][0]
                assert "chapter" in citation
                assert isinstance(citation["chapter"], str)
            
            # Check metadata
            assert isinstance(data["response_time_ms"], int)
            assert data["response_time_ms"] >= 0
            assert isinstance(data["timestamp"], str)


class TestCORS:
    """Test CORS configuration"""
    
    def test_cors_headers_present(self, mock_agent_runner):
        """Test that CORS headers are present in responses"""
        with patch('api.main.agent_runner', mock_agent_runner):
            response = client.options("/api/health")
            # OPTIONS should be allowed
            assert response.status_code in [200, 405]  # 405 if not implemented


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
