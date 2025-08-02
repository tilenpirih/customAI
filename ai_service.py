"""
AI Service module for handling Gemini API interactions with vector database context.
"""
from dotenv import load_dotenv
import os
import requests
from vector_db import VectorDatabase
from typing import Optional, Dict, Any

# Load environment variables
load_dotenv(".env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class AIService:
    def __init__(self):
        """Initialize the AI service with vector database."""
        self.vector_db = None
        self.is_initialized = False
    
    def initialize(self):
        """Initialize and populate the vector database with data."""
        if self.is_initialized:
            return
        
        self.vector_db = VectorDatabase()
        
        data_file = "data/data.json"
        if os.path.exists(data_file):
            # Check if collection is empty
            if self.vector_db.collection.count() == 0:
                print("Populating vector database with coaching data...")
                self.vector_db.load_and_index_data(data_file)
            else:
                print(f"Vector database already contains {self.vector_db.collection.count()} documents")
        else:
            print(f"Warning: {data_file} not found. Vector database will be empty.")
        
        self.is_initialized = True
    
    def get_relevant_context(self, query: str, max_length: int = 1000) -> str:
        """Get relevant context for the query."""
        if not self.is_initialized:
            self.initialize()
        
        return self.vector_db.get_enhanced_context(query, max_context_length=max_length)
    
    def make_gemini_request_with_context(self, prompt_text: str) -> Dict[str, Any]:
        """Make a request to Gemini API with relevant context from vector database."""
        if not self.is_initialized:
            self.initialize()
        
        # Get relevant context from vector database
        relevant_context = self.vector_db.get_enhanced_context(prompt_text)
        
        # Create enhanced prompt with context
        if relevant_context:
            enhanced_prompt = f"""Kontekst iz predpisov o trenerskih licencah:
{relevant_context}

Na podlagi zgornjega konteksta odgovori na naslednje vprašanje:
{prompt_text}

Odgovori v slovenščini in uporabi informacije iz konteksta, kjer je to relevantno."""
        else:
            enhanced_prompt = prompt_text
        
        return self._make_gemini_request(enhanced_prompt, context_used=relevant_context)
    
    def make_gemini_request(self, prompt_text: str) -> Dict[str, Any]:
        """Make a request to Gemini API without context."""
        return self._make_gemini_request(prompt_text, context_used=None)
    
    def _make_gemini_request(self, prompt_text: str, context_used: Optional[str] = None) -> Dict[str, Any]:
        """Internal method to make request to Gemini API."""
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
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                return {
                    "success": True,
                    "response": ai_response,
                    "context_used": context_used is not None,
                    "context": context_used[:500] + "..." if context_used and len(context_used) > 500 else context_used,
                    "error": None
                }
            else:
                return {
                    "success": False,
                    "response": None,
                    "context_used": False,
                    "context": None,
                    "error": "No response generated"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "response": None,
                "context_used": False,
                "context": None,
                "error": f"Error making request: {e}"
            }
        except KeyError as e:
            return {
                "success": False,
                "response": None,
                "context_used": False,
                "context": None,
                "error": f"Error parsing response: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "response": None,
                "context_used": False,
                "context": None,
                "error": f"Unexpected error: {e}"
            }

# Create a global instance
ai_service = AIService()
