# Document Indexer API

A FastAPI-based service for indexing and searching documents in Elasticsearch.

## Features

- **Index Management**: Create, delete, and check existence of Elasticsearch indices
- **Document Operations**: Index, retrieve, update, and delete documents
- **Bulk Operations**: Bulk index multiple documents for better performance
- **Search Capabilities**: Simple text search and advanced Elasticsearch query DSL support
- **Health Monitoring**: Health check endpoints for API and Elasticsearch connectivity

## Prerequisites

- Python 3.8+
- Elasticsearch server running (default: http://localhost:9200)

## Installation

1. Install dependencies:
```bash
pip install -r requirements
```

2. Set environment variables (optional):
```bash
export ELASTICSEARCH_HOST=http://localhost:9200
```

## Running the API

Start the FastAPI server:

```bash
# Using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Or run the app.py file directly
python app.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc

## API Endpoints

### Health & Version
- `GET /health` - Check API and Elasticsearch health
- `GET /api/version` - Get API version information

### Index Management
- `POST /api/indices` - Create a new index with mappings and settings
- `GET /api/indices/{index_name}/exists` - Check if an index exists
- `DELETE /api/indices/{index_name}` - Delete an index
- `POST /api/indices/{index_name}/refresh` - Refresh an index

### Document Operations
- `POST /api/documents/{index_name}` - Index a single document
- `POST /api/documents/bulk` - Bulk index multiple documents
- `GET /api/documents/{index_name}/{doc_id}` - Retrieve a document by ID
- `PUT /api/documents/{index_name}/{doc_id}` - Update a document
- `DELETE /api/documents/{index_name}/{doc_id}` - Delete a document
- `GET /api/documents/{index_name}/count` - Count documents in an index

### Search Operations
- `POST /api/search/{index_name}` - Simple text search
- `POST /api/search/{index_name}/advanced` - Advanced search with Elasticsearch query DSL

## Usage Examples

### Create an Index

```bash
curl -X POST "http://localhost:8000/api/indices" \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "my_documents",
    "mappings": {
      "properties": {
        "title": {"type": "text"},
        "content": {"type": "text"},
        "author": {"type": "keyword"},
        "tags": {"type": "keyword"}
      }
    }
  }'
```

### Index a Document

```bash
curl -X POST "http://localhost:8000/api/documents/my_documents" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Document",
    "content": "This is the content of my document",
    "author": "John Doe",
    "tags": ["example", "test"]
  }'
```

### Search Documents

```bash
curl -X POST "http://localhost:8000/api/search/my_documents" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "content document",
    "size": 10
  }'
```

## Document Model

The API expects documents to follow this structure:

```json
{
  "title": "Document Title",
  "content": "Document content text",
  "author": "Author Name (optional)",
  "tags": ["tag1", "tag2"],
  "metadata": {
    "custom_field": "custom_value"
  }
}
```

## Testing

Run the example usage script to test the API:

```bash
python example_usage.py
```

This script will:
1. Check API health
2. Create a test index
3. Index sample documents
4. Perform various search operations
5. Demonstrate document retrieval and counting

## Environment Variables

- `ELASTICSEARCH_HOST`: Elasticsearch server URL (default: http://localhost:9200)

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:
- `400 Bad Request`: Invalid input or index already exists
- `404 Not Found`: Index or document not found
- `500 Internal Server Error`: Server or Elasticsearch errors

## Development

To run in development mode with auto-reload:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Architecture

The API is built with:
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **Elasticsearch**: Search and analytics engine
- **Custom Elasticsearch Client**: Wrapper for Elasticsearch operations

The application follows a modular structure:
- `app.py`: Main FastAPI application with all endpoints
- `clients/elasticsearch_client.py`: Elasticsearch operations wrapper
- `example_usage.py`: Example script demonstrating API usage
