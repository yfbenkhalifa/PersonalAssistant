"""
Example usage of the Document Indexer API
This script demonstrates how to interact with the API endpoints
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_api():
    """Test the Document Indexer API"""
    
    # Test health check
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health status: {response.json()}")
    
    # Test version endpoint
    print("\nTesting version endpoint...")
    response = requests.get(f"{BASE_URL}/api/version")
    print(f"Version info: {response.json()}")
    
    # Create an index
    index_name = "test_documents"
    print(f"\nCreating index '{index_name}'...")
    index_config = {
        "index_name": index_name,
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "author": {"type": "keyword"},
                "tags": {"type": "keyword"},
                "created_at": {"type": "date"}
            }
        },
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/indices", json=index_config)
    if response.status_code == 200:
        print(f"Index created: {response.json()}")
    else:
        print(f"Failed to create index: {response.text}")
    
    # Index a document
    print(f"\nIndexing a document...")
    document = {
        "title": "Sample Document",
        "content": "This is a sample document for testing the indexing API.",
        "author": "Test Author",
        "tags": ["sample", "test", "demo"],
        "metadata": {
            "category": "test",
            "importance": "high"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/documents/{index_name}", json=document)
    if response.status_code == 200:
        result = response.json()
        print(f"Document indexed: {result}")
        doc_id = result["document_id"]
    else:
        print(f"Failed to index document: {response.text}")
        return
    
    # Bulk index documents
    print(f"\nBulk indexing documents...")
    bulk_request = {
        "index_name": index_name,
        "documents": [
            {
                "title": "Document 1",
                "content": "Content of the first document with some keywords",
                "author": "Author 1",
                "tags": ["bulk", "test"]
            },
            {
                "title": "Document 2", 
                "content": "Content of the second document with different keywords",
                "author": "Author 2",
                "tags": ["bulk", "demo"]
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/documents/bulk", json=bulk_request)
    if response.status_code == 200:
        print(f"Bulk indexing result: {response.json()}")
    else:
        print(f"Failed to bulk index: {response.text}")
    
    # Refresh index to make documents searchable
    print(f"\nRefreshing index...")
    response = requests.post(f"{BASE_URL}/api/indices/{index_name}/refresh")
    print(f"Refresh result: {response.json()}")
    
    # Search documents
    print(f"\nSearching documents...")
    search_query = {
        "query": "sample keywords",
        "size": 10
    }
    
    response = requests.post(f"{BASE_URL}/api/search/{index_name}", json=search_query)
    if response.status_code == 200:
        results = response.json()
        print(f"Search results: {json.dumps(results, indent=2)}")
    else:
        print(f"Search failed: {response.text}")
    
    # Get document by ID
    print(f"\nRetrieving document by ID...")
    response = requests.get(f"{BASE_URL}/api/documents/{index_name}/{doc_id}")
    if response.status_code == 200:
        print(f"Retrieved document: {response.json()}")
    else:
        print(f"Failed to retrieve document: {response.text}")
    
    # Count documents
    print(f"\nCounting documents...")
    response = requests.get(f"{BASE_URL}/api/documents/{index_name}/count")
    if response.status_code == 200:
        print(f"Document count: {response.json()}")
    else:
        print(f"Failed to count documents: {response.text}")
    
    # Advanced search example
    print(f"\nPerforming advanced search...")
    advanced_query = {
        "bool": {
            "should": [
                {"match": {"title": "Document"}},
                {"match": {"content": "keywords"}}
            ]
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/search/{index_name}/advanced", json=advanced_query)
    if response.status_code == 200:
        results = response.json()
        print(f"Advanced search results: {json.dumps(results, indent=2)}")
    else:
        print(f"Advanced search failed: {response.text}")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")
