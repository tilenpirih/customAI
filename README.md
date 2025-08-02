# CustomAI - Basketball Coaching License Assistant

A FastAPI-powered AI assistant that uses vector database to enhance Gemini API responses with relevant context from basketball coaching license regulations.

## Features

- **🚀 FastAPI REST API**: Modern, fast web API with automatic documentation
- **🔍 Vector Database Integration**: Uses ChromaDB to store and retrieve relevant context
- **🧠 Semantic Search**: Leverages sentence transformers for finding relevant information
- **🤖 Enhanced AI Responses**: Combines retrieved context with Gemini API for accurate answers
- **🌐 Web Interface**: Simple HTML frontend for testing
- **🔧 Multiple Endpoints**: Query with/without context, get context only, health checks
- **📚 Multilingual Support**: Works with Slovenian language content about basketball coaching licenses

## Setup

1. Create and activate virtual environment:

```bash
python3 -m venv venv
. venv/bin/activate
python3 -m pip install -r requirements.txt
```

2. Create a `.env` file with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

3. Ensure your `data/data.json` file contains the coaching license data

## Usage

### Start the API Server

```bash
python main.py
```

The API will be available at:

- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

### Web Interface

Open `frontend.html` in your browser for a simple web interface.

### API Endpoints

#### POST `/query`

Ask questions with optional context from vector database:

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "Kaj potrebujem da dobim licenco za trenerja?", "use_context": true}'
```

#### POST `/query-simple`

Simple endpoint that returns just the response text:

```bash
curl -X POST "http://localhost:8000/query-simple" \
     -H "Content-Type: application/json" \
     -d '{"query": "Kakšne vrste licenc obstajajo?"}'
```

#### POST `/context`

Get relevant context for a query without AI response:

```bash
curl -X POST "http://localhost:8000/context" \
     -H "Content-Type: application/json" \
     -d '{"query": "licence za trenerje", "max_length": 500}'
```

#### GET `/health`

Health check endpoint:

```bash
curl http://localhost:8000/health
```

### Test the API

Use the included test client:

```bash
python test_client.py
```

### Legacy Scripts (Still Available)

```bash
python examples.py      # Interactive demo
python db_manager.py    # Database management
```

## Files

- `main.py` - FastAPI server entry point
- `api.py` - FastAPI application with all endpoints
- `ai_service.py` - AI service module with Gemini API integration
- `vector_db.py` - Vector database class handling ChromaDB operations
- `test_client.py` - API test client
- `frontend.html` - Simple web interface for testing
- `examples.py` - Interactive demo (legacy)
- `db_manager.py` - Database management utility (legacy)
- `data/data.json` - Basketball coaching license data in SQuAD format

## How It Works

1. **Data Loading**: The system loads basketball coaching license data from JSON
2. **Indexing**: Documents are processed and indexed using sentence transformers
3. **Query Enhancement**: When you ask a question, relevant context is retrieved
4. **AI Response**: The context is combined with your query and sent to Gemini API
5. **Enhanced Answer**: You get a response that's grounded in the specific regulations

## Example Queries

- "Kaj potrebujem da dobim licenco za trenerja?" (What do I need to get a coach license?)
- "Kakšne vrste licenc obstajajo?" (What types of licenses exist?)
- "Kakšna licenca je potrebna za vodenje ekip v 1. SKL?" (What license is needed for 1st league teams?)

The system will automatically find relevant information from the regulations and provide accurate, context-aware responses.

fastapi, uvicorn, numpy, chromadb, sentence-transformers
