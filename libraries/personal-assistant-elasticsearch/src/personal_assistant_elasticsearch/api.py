from __future__ import annotations

import os
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException

from .clients import ElasticSearchClient
from .document_chunking import DumbDocumentChunker
from .dto import DocumentModel, IndexConfig
from .request_models import BulkIndexRequest, SearchQuery
from .settings import SearchServiceSettings, default_settings_path
from .text_encoder import SentenceTransformerTextEncoder


class SearchRuntime:
    def __init__(
        self,
        settings: SearchServiceSettings,
        client: ElasticSearchClient | None = None,
        text_encoder: SentenceTransformerTextEncoder | None = None,
    ) -> None:
        self.settings = settings
        self.es_client = client or ElasticSearchClient(
            host=settings.elasticsearch_host,
            port=settings.elasticsearch_port,
            user=settings.elasticsearch_username,
            password=settings.elasticsearch_password,
            api_key=settings.elasticsearch_api_key,
        )
        self.text_encoder = text_encoder

    def get_text_encoder(self):
        if self.text_encoder is None:
            self.text_encoder = SentenceTransformerTextEncoder(self.settings.text_encoder_model_name)
        return self.text_encoder


SETTINGS_PATH = Path(
    os.getenv("PERSONAL_ASSISTANT_ELASTICSEARCH_SETTINGS", str(default_settings_path()))
)
DEFAULT_RUNTIME = SearchRuntime(SearchServiceSettings.from_yaml(SETTINGS_PATH))


def create_app(runtime: SearchRuntime | None = None) -> FastAPI:
    local_runtime = runtime or DEFAULT_RUNTIME
    app = FastAPI(
        title=local_runtime.settings.api_title,
        description=local_runtime.settings.api_description,
        version=local_runtime.settings.api_version,
    )

    @app.get("/api/version")
    async def version():
        return {
            "version": local_runtime.settings.api_version,
            "service": local_runtime.settings.api_title,
            "elasticsearch_host": local_runtime.settings.elasticsearch_host,
        }

    @app.get("/health")
    async def health_check():
        es_healthy = local_runtime.es_client.health_check()
        return {
            "status": "healthy" if es_healthy else "unhealthy",
            "elasticsearch": "connected" if es_healthy else "disconnected",
            "host": local_runtime.settings.elasticsearch_host,
        }

    @app.post("/api/indices")
    async def create_index(config: IndexConfig):
        if local_runtime.es_client.index_exists(config.index_name):
            raise HTTPException(status_code=400, detail=f"Index '{config.index_name}' already exists")

        success = local_runtime.es_client.create_index(
            index_name=config.index_name,
            mapping=config.mappings,
            settings=config.settings,
        )
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create index")
        return {"message": f"Index '{config.index_name}' created successfully"}

    @app.get("/api/indices/{index_name}/exists")
    async def check_index_exists(index_name: str):
        return {"index_name": index_name, "exists": local_runtime.es_client.index_exists(index_name)}

    @app.delete("/api/indices/{index_name}")
    async def delete_index(index_name: str):
        if not local_runtime.es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        success = local_runtime.es_client.delete_index(index_name)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete index")
        return {"message": f"Index '{index_name}' deleted successfully"}

    @app.post("/api/indices/{index_name}/refresh")
    async def refresh_index(index_name: str):
        if not local_runtime.es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        success = local_runtime.es_client.refresh_index(index_name)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to refresh index")
        return {"message": f"Index '{index_name}' refreshed successfully"}

    @app.post("/api/documents/{index_name}")
    async def index_document(index_name: str, document: DocumentModel, doc_id: str | None = None):
        if not local_runtime.es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")

        chunker = DumbDocumentChunker(local_runtime.settings.max_document_length)
        chunks = chunker.chunk_document(document.content)
        encoder = local_runtime.get_text_encoder()
        response = None
        for chunk in chunks:
            payload = document.model_dump()
            payload["content"] = chunk["content"]
            embeddings = encoder.encode(chunk["content"])
            response = local_runtime.es_client.index_document(index_name, payload, doc_id, embeddings=embeddings)

        return {
            "message": "Document indexed successfully",
            "document_id": response["_id"] if response else doc_id,
            "result": response.get("result") if response else "created",
        }

    @app.post("/api/documents/bulk")
    async def bulk_index_documents(request: BulkIndexRequest):
        if not local_runtime.es_client.index_exists(request.index_name):
            raise HTTPException(status_code=404, detail=f"Index '{request.index_name}' not found")
        result = local_runtime.es_client.bulk_index_documents(
            request.index_name,
            [doc.model_dump() for doc in request.documents],
        )
        return {
            "message": "Bulk indexing completed",
            **result,
        }

    @app.get("/api/documents/{index_name}/{doc_id}")
    async def get_document(index_name: str, doc_id: str):
        if not local_runtime.es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        document = local_runtime.es_client.get_document(index_name, doc_id)
        if document is None:
            raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")
        return {"document_id": doc_id, "document": document}

    @app.put("/api/documents/{index_name}/{doc_id}")
    async def update_document(index_name: str, doc_id: str, update_data: dict = Body(...)):
        if not local_runtime.es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        response = local_runtime.es_client.update_document(index_name, doc_id, update_data)
        return {
            "message": "Document updated successfully",
            "document_id": doc_id,
            "result": response["result"],
        }

    @app.delete("/api/documents/{index_name}/{doc_id}")
    async def delete_document(index_name: str, doc_id: str):
        if not local_runtime.es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        success = local_runtime.es_client.delete_document(index_name, doc_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Document '{doc_id}' not found")
        return {"message": f"Document '{doc_id}' deleted successfully"}

    @app.get("/api/documents/{index_name}/count")
    async def count_documents(index_name: str):
        if not local_runtime.es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        count = local_runtime.es_client.count_documents(index_name)
        return {"index_name": index_name, "count": count}

    @app.post("/api/search/{index_name}")
    async def search_documents(index_name: str, search_query: SearchQuery):
        if not local_runtime.es_client.index_exists(index_name):
            raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")
        results = local_runtime.es_client.simple_search(
            index_name=index_name,
            search_text=search_query.query,
            fields=search_query.fields,
            size=search_query.size,
            from_=search_query.from_,
        )
        return {"index_name": index_name, "results": results, "count": len(results)}

    return app


app = create_app()


