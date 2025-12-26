"""Test FastAPI backend"""

import requests
import time

def test_api():
    """Test FastAPI backend endpoints"""
    print("\n=== Testing FastAPI Backend ===\n")
    
    BASE_URL = "http://localhost:8000"
    
    # Test 1: Health Check
    print("1. Testing /api/health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Status: {data.get('status')}")
            checks = data.get('checks', {})
            print(f"   - API Running: {checks.get('api_running')}")
            print(f"   - Agent Loaded: {checks.get('agent_loaded')}")
            print(f"   - Embeddings Loaded: {checks.get('embeddings_loaded')}")
        print()
    except requests.exceptions.ConnectionError:
        print("   ❌ Error: Backend server not running!")
        print("   Please start the backend with: cd backend && uvicorn api.main:app --reload\n")
        return
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        return
    
    # Test 2: Stats Endpoint
    print("2. Testing /api/stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Database Stats:")
            print(f"   - Total Chunks: {data.get('total_chunks')}")
            print(f"   - Modules: {data.get('modules')}")
            print(f"   - Chapters: {data.get('chapters')}")
            print(f"   - Topics: {data.get('topics')}")
        print()
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
    
    # Test 3: Chat Endpoint
    print("3. Testing /api/chat endpoint...")
    test_questions = [
        "What is Physical AI?",
        "Explain ROS 2 architecture",
        "Why do we need simulation?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n   Test {i}: {question}")
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/api/chat",
                json={"question": question},
                timeout=30
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                response_time = end_time - start_time
                print(f"   ✅ Response received in {response_time:.2f}s")
                print(f"   Answer preview: {data.get('answer', '')[:150]}...")
                citations = data.get('citations', [])
                print(f"   Citations: {len(citations)} sources")
                if citations:
                    print(f"   - {citations[0].get('title', 'Unknown')}")
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n\n✅ API testing completed!\n")

if __name__ == "__main__":
    test_api()
