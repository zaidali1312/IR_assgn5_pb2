from src.search_engine import SearchEngine
import sys
import os

if __name__ == "__main__":
    # Define the data directory
    data_dir = "./data/"
    
    # Initialize the search engine
    engine = SearchEngine()
    
    # Build the index
    print("Building the index...")
    engine.build_index(data_dir)
    print(f"Indexed {engine.N} documents.")
    
    # Accept user query
    query = input("Enter your query: ")
    
    # Perform search
    print(f"Searching for: {query}")
    results = engine.search(query)
    
    # Display results
    print("\nTop Results:")
    for file_name, score in results:
        print(f"File: {file_name}, Score: {score}")
