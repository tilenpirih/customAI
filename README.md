# CustomAI - Basketball Coaching License Assistant

A custom AI project that uses vector database to enhance Gemini API responses with relevant context from basketball coaching license regulations.

## Features

- **Vector Database Integration**: Uses ChromaDB to store and retrieve relevant context
- **Semantic Search**: Leverages sentence transformers for finding relevant information
- **Enhanced AI Responses**: Combines retrieved context with Gemini API for accurate answers
- **Multilingual Support**: Works with Slovenian language content about basketball coaching licenses

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

### Basic Usage

Run the main script to see an example query:

```bash
python main.py
```

### Interactive Demo

Try different queries with the examples script:

```bash
python examples.py
```

### Database Management

Use the database manager to initialize, test, or manage your vector database:

```bash
python db_manager.py
```

## Files

- `main.py` - Main script with enhanced Gemini API integration
- `vector_db.py` - Vector database class handling ChromaDB operations
- `examples.py` - Interactive demo and example queries
- `db_manager.py` - Utility for managing the vector database
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
