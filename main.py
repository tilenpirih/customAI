from dotenv import load_dotenv
import os
import asyncio
import requests
import json
from vector_db import VectorDatabase

load_dotenv(".env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize vector database
vector_db = VectorDatabase()

def initialize_vector_db():
    """Initialize and populate the vector database with data."""
    data_file = "data/data.json"
    if os.path.exists(data_file):
        # Check if collection is empty
        if vector_db.collection.count() == 0:
            print("Populating vector database with coaching data...")
            vector_db.load_and_index_data(data_file)
        else:
            print(f"Vector database already contains {vector_db.collection.count()} documents")
    else:
        print(f"Warning: {data_file} not found. Vector database will be empty.")

def make_gemini_request_with_context(prompt_text):
    """Make a request to Gemini API with relevant context from vector database."""
    # Get relevant context from vector database
    relevant_context = vector_db.get_enhanced_context(prompt_text)
    
    # Create enhanced prompt with context
    if relevant_context:
        enhanced_prompt = f"""Kontekst iz mojih podatkov:
        {relevant_context}

        Na podlagi zgornjega konteksta odgovori na naslednje vprašanje:
        {prompt_text}

        Odgovori v slovenščini in uporabi informacije iz konteksta, kjer je to relevantno.
        """
    else:
        enhanced_prompt = prompt_text
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": enhanced_prompt
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "No response generated"
            
    except requests.exceptions.RequestException as e:
        return f"Error making request: {e}"
    except KeyError as e:
        return f"Error parsing response: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def make_gemini_request(prompt_text):
    """Original function for requests without context (kept for compatibility)."""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "No response generated"
            
    except requests.exceptions.RequestException as e:
        return f"Error making request: {e}"
    except KeyError as e:
        return f"Error parsing response: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

async def main():
    # Initialize vector database
    initialize_vector_db()
    
    prompt = "Kaj potrebujem da dobim licenco za trenerja?"
    print("Making request to Gemini API with vector database context...")
    
    # Use the enhanced function with context
    result = make_gemini_request_with_context(prompt)
    
    print("\nResponse from Gemini (with relevant context):")
    print("=" * 50)
    print(result)
    print("=" * 50)
    
    # Optional: Show what context was retrieved
    print("\nRelevant context used:")
    print("-" * 30)
    context = vector_db.get_enhanced_context(prompt, max_context_length=500)
    print(context[:500] + "..." if len(context) > 500 else context)

if __name__ == "__main__":
    asyncio.run(main())
