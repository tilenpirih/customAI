import chromadb
import json
from sentence_transformers import SentenceTransformer
import os
from typing import List, Dict, Any

class VectorDatabase:
    def __init__(self, collection_name: str = "basketball_coaching", persist_directory: str = "./chroma_db"):
        """Initialize the vector database with ChromaDB and sentence transformers."""
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight multilingual model
        self.collection_name = collection_name
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Loaded existing collection '{collection_name}' with {self.collection.count()} documents")
        except Exception:  # Collection doesn't exist
            self.collection = self.client.create_collection(name=collection_name)
            print(f"Created new collection '{collection_name}'")
    
    def load_and_index_data(self, json_file_path: str):
        """Load data from JSON file and index it in the vector database."""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        documents = []
        metadatas = []
        ids = []
        
        doc_id = 0
        
        for item in data['data']:
            title = item['title']
            
            for paragraph in item['paragraphs']:
                context = paragraph['context']
                
                # Add the main context
                documents.append(context)
                metadatas.append({
                    "title": title,
                    "type": "context",
                    "source": "coaching_regulations"
                })
                ids.append(f"context_{doc_id}")
                doc_id += 1
                
                # Add Q&A pairs for better retrieval
                for qa in paragraph['qas']:
                    question = qa['question']
                    
                    # Combine question with answers for better context
                    if qa['answers']:
                        answer_texts = [ans['text'] for ans in qa['answers']]
                        combined_qa = f"Q: {question} A: {' | '.join(answer_texts)}"
                    else:
                        combined_qa = f"Q: {question}"
                    
                    documents.append(combined_qa)
                    metadatas.append({
                        "title": title,
                        "type": "qa",
                        "question": question,
                        "source": "coaching_regulations"
                    })
                    ids.append(f"qa_{doc_id}")
                    doc_id += 1
        
        # Generate embeddings and add to collection
        print(f"Indexing {len(documents)} documents...")
        
        # Add documents in batches to avoid memory issues
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_meta = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            embeddings = self.model.encode(batch_docs).tolist()
            
            self.collection.add(
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids,
                embeddings=embeddings
            )
        
        print(f"Successfully indexed {len(documents)} documents!")
    
    def search_relevant_context(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Search for relevant context based on the query."""
        # Generate embedding for the query
        query_embedding = self.model.encode([query]).tolist()[0]
        
        # Search in the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )
        
        # Format results
        relevant_docs = []
        for i, doc in enumerate(results['documents'][0]):
            relevant_docs.append({
                'content': doc,
                'metadata': results['metadatas'][0][i],
                'similarity_score': 1 - results['distances'][0][i]  # Convert distance to similarity
            })
        
        return relevant_docs
    
    def get_enhanced_context(self, query: str, max_context_length: int = 1000) -> str:
        """Get relevant context for enhancing the query."""
        relevant_docs = self.search_relevant_context(query, n_results=5)
        
        context_parts = []
        current_length = 0
        
        for doc in relevant_docs:
            content = doc['content']
            title = doc['metadata'].get('title', '')
            
            # Format the context piece
            if doc['metadata']['type'] == 'context':
                formatted_content = f"[{title}] {content}"
            else:
                formatted_content = f"[{title}] {content}"
            
            # Check if adding this would exceed max length
            if current_length + len(formatted_content) > max_context_length:
                break
            
            context_parts.append(formatted_content)
            current_length += len(formatted_content)
        
        return "\n\n".join(context_parts)
    
    def clear_collection(self):
        """Clear all data from the collection."""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(name=self.collection_name)
        print("Collection cleared!")
