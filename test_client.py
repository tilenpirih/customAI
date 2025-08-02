#!/usr/bin/env python3
"""
Test client for the Basketball Coaching License Assistant API.
Use this to test the API endpoints.
"""
import requests
import json
from typing import Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def query_with_context(self, query: str) -> Dict[str, Any]:
        """Send a query with context to the API."""
        response = requests.post(
            f"{self.base_url}/query",
            json={"query": query, "use_context": True}
        )
        return response.json()
    
    def query_without_context(self, query: str) -> Dict[str, Any]:
        """Send a query without context to the API."""
        response = requests.post(
            f"{self.base_url}/query",
            json={"query": query, "use_context": False}
        )
        return response.json()
    
    def query_simple(self, query: str) -> Dict[str, Any]:
        """Send a simple query to the API."""
        response = requests.post(
            f"{self.base_url}/query-simple",
            json={"query": query, "use_context": True}
        )
        return response.json()
    
    def get_context(self, query: str, max_length: int = 1000) -> Dict[str, Any]:
        """Get relevant context for a query."""
        response = requests.post(
            f"{self.base_url}/context",
            json={"query": query, "max_length": max_length}
        )
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_examples(self) -> Dict[str, Any]:
        """Get example queries."""
        response = requests.get(f"{self.base_url}/example")
        return response.json()

def test_api():
    """Test the API with sample queries."""
    client = APIClient()
    
    print("🏀 Testing Basketball Coaching License Assistant API")
    print("=" * 60)
    
    # Health check
    print("\n1. Health Check:")
    try:
        health = client.health_check()
        print(f"Status: {health['status']}")
        print(f"AI Service Initialized: {health['ai_service_initialized']}")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the API server is running (python main.py)")
        return
    
    # Get examples
    print("\n2. Available Examples:")
    examples = client.get_examples()
    for i, example in enumerate(examples['example_queries'][:3], 1):
        print(f"   {i}. {example}")
    
    # Test queries
    test_queries = [
        "Kaj potrebujem da dobim licenco za trenerja?",
        "Kakšne vrste licenc obstajajo?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i+2}. Testing Query: '{query}'")
        print("-" * 40)
        
        # Test with context
        try:
            result = client.query_with_context(query)
            if result['success']:
                print(f"✅ Response: {result['response'][:150]}...")
                if result['context_used']:
                    print(f"📖 Context used: {len(result['context']) if result['context'] else 0} characters")
            else:
                print(f"❌ Error: {result['error']}")
        except Exception as e:
            print(f"❌ Request error: {e}")

def interactive_test():
    """Interactive testing mode."""
    client = APIClient()
    
    print("🤖 Interactive API Testing Mode")
    print("Type 'quit' to exit, 'context <query>' to get context only")
    print("=" * 50)
    
    while True:
        query = input("\n💬 Your question: ").strip()
        
        if query.lower() == 'quit':
            print("Goodbye! 👋")
            break
        
        if query.lower().startswith('context '):
            # Get context only
            search_query = query[8:]
            try:
                result = client.get_context(search_query)
                print(f"\n🔍 Context for '{search_query}':")
                print("-" * 30)
                print(result['context'])
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif query:
            # Regular query
            try:
                result = client.query_with_context(query)
                if result['success']:
                    print(f"\n🤖 Response:")
                    print("-" * 20)
                    print(result['response'])
                    if result['context_used']:
                        print(f"\n📖 Used context: {len(result['context']) if result['context'] else 0} chars")
                else:
                    print(f"❌ Error: {result['error']}")
            except Exception as e:
                print(f"❌ Request error: {e}")

if __name__ == "__main__":
    print("Choose testing mode:")
    print("1. Automated test")
    print("2. Interactive test")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_api()
    elif choice == "2":
        interactive_test()
    else:
        print("Invalid choice. Run the script again.")
