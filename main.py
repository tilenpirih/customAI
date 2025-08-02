"""
Main entry point for the Basketball Coaching License Assistant API.
Run this file to start the FastAPI server.
"""
import uvicorn

if __name__ == "__main__":
    print("🏀 Starting Basketball Coaching License Assistant API...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
    print("🔧 Alternative docs: http://localhost:8000/redoc")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
