#!/usr/bin/env python3
"""
Utility script for managing the vector database.
Run this script to initialize, test, or manage your vector database.
"""

from vector_db import VectorDatabase
import os

def main():
    print("=== Vector Database Manager ===")
    
    # Initialize vector database
    vector_db = VectorDatabase()
    
    while True:
        print("\nOptions:")
        print("1. Load data from data.json")
        print("2. Test search functionality")
        print("3. Show database stats")
        print("4. Clear database")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            data_file = "data/data.json"
            if os.path.exists(data_file):
                print("Loading and indexing data...")
                vector_db.load_and_index_data(data_file)
                print("Data loaded successfully!")
            else:
                print(f"Error: {data_file} not found!")
        
        elif choice == "2":
            query = input("Enter search query: ").strip()
            if query:
                print(f"\nSearching for: '{query}'")
                results = vector_db.search_relevant_context(query, n_results=3)
                
                for i, result in enumerate(results, 1):
                    print(f"\n--- Result {i} ---")
                    print(f"Title: {result['metadata'].get('title', 'N/A')}")
                    print(f"Type: {result['metadata'].get('type', 'N/A')}")
                    print(f"Similarity: {result['similarity_score']:.3f}")
                    print(f"Content: {result['content'][:200]}...")
        
        elif choice == "3":
            count = vector_db.collection.count()
            print(f"\nDatabase contains {count} documents")
            
            if count > 0:
                # Show sample of metadata
                sample = vector_db.collection.peek(limit=5)
                print("\nSample documents:")
                for i, (doc, meta) in enumerate(zip(sample['documents'], sample['metadatas'])):
                    print(f"{i+1}. [{meta.get('title', 'N/A')}] {doc[:100]}...")
        
        elif choice == "4":
            confirm = input("Are you sure you want to clear all data? (yes/no): ").strip().lower()
            if confirm == "yes":
                vector_db.clear_collection()
                print("Database cleared!")
            else:
                print("Operation cancelled.")
        
        elif choice == "5":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
