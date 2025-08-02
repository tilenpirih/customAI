#!/usr/bin/env python3
"""
Example script showing different ways to use the vector database enhanced Gemini API.
"""

from dotenv import load_dotenv
import os
import asyncio
from main import make_gemini_request_with_context, initialize_vector_db, vector_db

load_dotenv(".env")

async def demo_queries():
    """Demonstrate the system with various queries."""
    
    print("Initializing vector database...")
    initialize_vector_db()
    
    # Example queries in Slovenian about basketball coaching licenses
    test_queries = [
        "Kaj potrebujem da dobim licenco za trenerja?",
        "Kakšne vrste licenc obstajajo?",
        "Kakšna licenca je potrebna za vodenje ekip v 1. SKL?",
        "Kdo lahko pridobi trenersko licenco?",
        "Kateri strokovni nazivi obstajajo za trenerje?",
        "Kaj je potrebno za vodenje mladinskih ekip?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"QUERY {i}: {query}")
        print('='*60)
        
        # Show relevant context that will be used
        print("\n🔍 RELEVANT CONTEXT:")
        context = vector_db.get_enhanced_context(query, max_context_length=300)
        print(context)
        
        print("\n🤖 GEMINI RESPONSE:")
        response = make_gemini_request_with_context(query)
        print(response)
        
        # Wait a bit between queries to be nice to the API
        await asyncio.sleep(1)

async def interactive_mode():
    """Interactive mode for testing queries."""
    print("Initializing vector database...")
    initialize_vector_db()
    
    print("\n🎯 Interactive Mode - Ask questions about basketball coaching licenses!")
    print("Type 'quit' to exit, 'context <query>' to see only context, or just ask a question.")
    
    while True:
        query = input("\n💬 Your question: ").strip()
        
        if query.lower() == 'quit':
            print("Goodbye! 👋")
            break
        
        if query.lower().startswith('context '):
            # Show only the context that would be retrieved
            search_query = query[8:]  # Remove 'context ' prefix
            context = vector_db.get_enhanced_context(search_query)
            print(f"\n🔍 Context for '{search_query}':")
            print("-" * 40)
            print(context)
        
        elif query:
            print(f"\n🤖 Response for: {query}")
            print("-" * 40)
            response = make_gemini_request_with_context(query)
            print(response)

if __name__ == "__main__":
    print("🏀 Basketball Coaching License Assistant")
    print("This demo shows how vector database enhances AI responses.")
    
    mode = input("\nChoose mode:\n1. Demo with predefined queries\n2. Interactive mode\nEnter choice (1 or 2): ").strip()
    
    if mode == "1":
        asyncio.run(demo_queries())
    elif mode == "2":
        asyncio.run(interactive_mode())
    else:
        print("Invalid choice. Run the script again.")
