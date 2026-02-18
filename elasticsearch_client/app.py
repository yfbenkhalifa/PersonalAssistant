from document_chunking.dumb_document_chunker import DumbDocumentChunker
from text_encoder import SentenceTransformerTextEncoder
from dto import DocumentModel, IndexConfig
from request_models import BulkIndexRequest, SearchQuery
from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import os
from loguru import logger
from clients.elasticsearch_client import ElasticSearchClient

from appSettings import AppSettings as settings

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Initialize Elasticsearch client
try: 
    es_client = ElasticSearchClient(host=settings.ELASTICSEARCH_HOST, port=settings.ELASTICSEARCH_PORT,
                                    user=settings.ELASTICSEARCH_USERNAME, api_key=settings.ELASTICSEARCH_API_KEY)
except Exception as e:
    logger.error(f"Failed to create ES client: {e}")

try:
    text_encoder = SentenceTransformerTextEncoder(settings.TEXTENCODER_MODELNAME)
except Exception as e:
    logger.error(f"Failed to create Text encoder: {e}")

@app.get("/api/version")
async def version():
    """Get API version information"""
    return {
        "version": settings.API_VERSION,
        "service": settings.API_TITLE,
        "elasticsearch_host": settings.ELASTICSEARCH_HOST
    }

@app.get("/health")
async def health_check():
    """Check the health of the API and Elasticsearch connection"""
    es_healthy = es_client.health_check()
    return {
        "status": "healthy" if es_healthy else "unhealthy",
        "elasticsearch": "connected" if es_healthy else "disconnected",
        "host": settings.ELASTICSEARCH_HOST
    }

# Index Management Endpoints
@app.post("/api/indices")
async def create_index(config: IndexConfig):
    """Create a new Elasticsearch index with optional mappings and settings"""
    try:
        if es_client.index_exists(config.index_name):
            raise HTTPException(status_code=400, detail=f"Index '{config.index_name}' already exists")
        
        success = es_client.create_index(
            index_name=config.index_name,
            mapping=config.mappings,
            settings=config.settings
        )
        
        if success:
            return {"message": f"Index '{config.index_name}' created successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to create index")
    except Exception as e:
        logger.error(f"Error creating index: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/indices/{index_name}/exists")
async def check_index_exists(index_name: str):
    """Check if an index exists"""
    exists = es_client.index_exists(index_name)
    return {"index_name": index_name, "exists": exists}

@app.delete("/api/indices/{index_name}")
async def delete_index(index_name: str):
    """Delete an Elasticsearch index"""
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        success = es_client.delete_index(index_name)
        if success:
            return {"message": f"Index '{index_name}' deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete index")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting index: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Document Management Endpoints
@app.post("/api/documents/{index_name}")
async def index_document(index_name: str, document: DocumentModel, doc_id: Optional[str] = None):
    """Index a single document"""
    document_chunker = DumbDocumentChunker(settings.MAX_DOCUMENT_LENGTH)
    document_chunks = [document_chunker.chunk_document(document.content)]
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        doc_dict = document.model_dump()
        for chunk in document_chunks:
            embeddings = text_encoder.encode(chunk[0]['content'])
            doc_dict["content"] = chunk
            response = es_client.index_document(index_name, doc_dict, doc_id, embeddings=embeddings)
        
        return {
            "message": "Document indexed successfully",
            "document_id": response["_id"],
            "result": response["result"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error indexing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/documents/chunk_document")
async def chunk_document(content: str):
    from clients.llm_client import AgenticDocumentChunker
    """Chunk a document using the AgenticDocumentChunker"""

    host = settings.AGENTIC_DOCUMENT_CHUNKER_HOST
    port = settings.AGENTIC_DOCUMENT_CHUNKER_PORT
    api_key = settings.AGENTIC_DOCUMENT_CHUNKER_API_KEY
    document_chunker = DumbDocumentChunker(4096)
    
    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty")

    result = document_chunker.chunk_document(content)
    return result

@app.post("/api/documents/bulk")
async def bulk_index_documents(request: BulkIndexRequest):
    """Bulk index multiple documents"""
    try:
        if not es_client.index_exists(request.index_name):
            raise HTTPException(status_code=404, detail=f"Index '{request.index_name}' not found")
        
        documents = [doc.model_dump() for doc in request.documents]
        result = es_client.bulk_index_documents(request.index_name, documents)
        
        return {
            "message": "Bulk indexing completed",
            "success_count": result["success_count"],
            "failed_count": result["failed_count"],
            "failed_items": result["failed_items"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error bulk indexing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/{index_name}/{doc_id}")
async def get_document(index_name: str, doc_id: str):
    """Retrieve a document by its ID"""
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        document = es_client.get_document(index_name, doc_id)
        if document is None:
            raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")
        
        return {"document_id": doc_id, "document": document}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/documents/{index_name}/{doc_id}")
async def update_document(index_name: str, doc_id: str, update_data: Dict[str, Any] = Body(...)):
    """Update a document by its ID"""
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        response = es_client.update_document(index_name, doc_id, update_data)
        
        return {
            "message": "Document updated successfully",
            "document_id": doc_id,
            "result": response["result"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/documents/{index_name}/{doc_id}")
async def delete_document(index_name: str, doc_id: str):
    """Delete a document by its ID"""
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        success = es_client.delete_document(index_name, doc_id)
        if success:
            return {"message": f"Document '{doc_id}' deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Search Endpoints
@app.post("/api/search/{index_name}")
async def search_documents(index_name: str, search_query: SearchQuery):
    """Search for documents using a text query"""
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        results = es_client.simple_search(
            index_name=index_name,
            search_text=search_query.query,
            fields=search_query.fields,
            size=search_query.size
        )
        
        return {
            "query": search_query.query,
            "total_results": len(results),
            "results": results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search/{index_name}/advanced")
async def advanced_search(index_name: str, query: Dict[str, Any] = Body(...), size: int = Query(settings.DEFAULT_SEARCH_SIZE, ge=1, le=settings.MAX_SEARCH_SIZE), from_: int = Query(0, ge=0, alias="from")):
    """Advanced search using Elasticsearch query DSL"""
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        response = es_client.search_documents(index_name, query, size, from_)
        
        return {
            "took": response["took"],
            "total": response["hits"]["total"],
            "max_score": response["hits"]["max_score"],
            "hits": [
                {
                    "id": hit["_id"],
                    "score": hit["_score"],
                    "source": hit["_source"]
                }
                for hit in response["hits"]["hits"]
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error performing advanced search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/{index_name}/count")
async def count_documents(index_name: str):
    """Count total number of documents in an index"""
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        count = es_client.count_documents(index_name)
        return {"index_name": index_name, "document_count": count}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error counting documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/indices/{index_name}/refresh")
async def refresh_index(index_name: str):
    """Refresh an index to make recent changes searchable"""
    try:
        if not es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        
        success = es_client.refresh_index(index_name)
        if success:
            return {"message": f"Index '{index_name}' refreshed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to refresh index")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing index: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)