"""
FastAPI application for the Basketball Coaching License Assistant.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ai_service import ai_service
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Basketball Coaching License Assistant",
    description="AI-powered assistant for basketball coaching license questions using vector database",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    use_context: bool = True

class QueryResponse(BaseModel):
    success: bool
    response: Optional[str]
    context_used: bool
    context: Optional[str]
    error: Optional[str]

class ContextRequest(BaseModel):
    query: str
    max_length: int = 1000

class ContextResponse(BaseModel):
    context: str
    query: str

# Initialize the AI service on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the AI service when the app starts."""
    print("Initializing AI service...")
    ai_service.initialize()
    print("AI service initialized successfully!")

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Basketball Coaching License Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "query": "/query - Ask questions with context",
            "query_simple": "/query-simple - Ask questions without context",
            "context": "/context - Get relevant context for a query",
            "health": "/health - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "ai_service_initialized": ai_service.is_initialized
    }

@app.post("/query", response_model=QueryResponse)
async def query_with_context(request: QueryRequest):
    """
    Ask a question to the AI with relevant context from the vector database.
    
    Args:
        request: QueryRequest containing the query and context preference
    
    Returns:
        QueryResponse with the AI response and context information
    """
    try:
        if request.use_context:
            result = ai_service.make_gemini_request_with_context(request.query)
        else:
            result = ai_service.make_gemini_request(request.query)
        
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/query-simple")
async def query_simple(request: QueryRequest):
    """
    Simple query endpoint that returns just the response text.
    
    Args:
        request: QueryRequest containing the query
    
    Returns:
        Dict with just the response text
    """
    try:
        if request.use_context:
            result = ai_service.make_gemini_request_with_context(request.query)
        else:
            result = ai_service.make_gemini_request(request.query)
        
        if result["success"]:
            return {"response": result["response"]}
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/context", response_model=ContextResponse)
async def get_context(request: ContextRequest):
    """
    Get relevant context for a query without making an AI request.
    
    Args:
        request: ContextRequest containing the query and max length
    
    Returns:
        ContextResponse with the relevant context
    """
    try:
        context = ai_service.get_relevant_context(request.query, request.max_length)
        return ContextResponse(context=context, query=request.query)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Example usage endpoint
@app.get("/example")
async def example_queries():
    """Get example queries that work well with this system."""
    return {
        "example_queries": [
            "Kaj potrebujem da dobim licenco za trenerja?",
            "Kakšne vrste licenc obstajajo?",
            "Kakšna licenca je potrebna za vodenje ekip v 1. SKL?",
            "Kdo lahko pridobi trenersko licenco?",
            "Kateri strokovni nazivi obstajajo za trenerje?",
            "Kaj je potrebno za vodenje mladinskih ekip?"
        ],
        "usage": "Send a POST request to /query with one of these queries"
    }

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
