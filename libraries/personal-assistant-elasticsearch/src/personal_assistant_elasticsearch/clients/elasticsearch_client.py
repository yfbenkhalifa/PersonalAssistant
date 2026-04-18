from __future__ import annotations

from typing import Any

import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticSearchClient:
    def __init__(
        self,
        host: str,
        port: int,
        api_key: str | None = None,
        user: str | None = None,
        password: str | None = None,
        verify_certs: bool = False,
        client: Elasticsearch | None = None,
    ) -> None:
        self.client = client or self._build_client(
            host=host,
            port=port,
            api_key=api_key,
            user=user,
            password=password,
            verify_certs=verify_certs,
        )

    @staticmethod
    def _build_client(
        host: str,
        port: int,
        api_key: str | None,
        user: str | None,
        password: str | None,
        verify_certs: bool,
    ) -> Elasticsearch:
        if api_key:
            base_url = host if host.startswith("http") else f"https://{host}"
            return Elasticsearch(
                hosts=[f"{base_url}:{port}"],
                api_key=api_key,
                verify_certs=verify_certs,
                ssl_show_warn=False,
            )

        base_url = host if host.startswith("http") else f"http://{host}"
        kwargs: dict[str, Any] = {
            "hosts": [f"{base_url}:{port}"],
            "verify_certs": verify_certs,
            "ssl_show_warn": False,
        }
        if user is not None and password is not None:
            kwargs["basic_auth"] = (user, password)
        return Elasticsearch(**kwargs)

    def health_check(self) -> bool:
        try:
            health = self.client.cluster.health()
            return health["status"] in {"green", "yellow"}
        except Exception:
            return False

    def create_index(
        self,
        index_name: str,
        mapping: dict[str, Any] | None = None,
        settings: dict[str, Any] | None = None,
    ) -> bool:
        body: dict[str, Any] = {}
        if mapping:
            body["mappings"] = mapping
        if settings:
            body["settings"] = settings
        response = self.client.indices.create(index=index_name, **({"body": body} if body else {}))
        return response.get("acknowledged", False)

    def index_exists(self, index_name: str) -> bool:
        return bool(self.client.indices.exists(index=index_name))

    def delete_index(self, index_name: str) -> bool:
        response = self.client.indices.delete(index=index_name)
        return response.get("acknowledged", False)

    def index_document(
        self,
        index_name: str,
        document: dict[str, Any],
        doc_id: str | None = None,
        embeddings: np.ndarray | None = None,
    ) -> dict[str, Any]:
        payload = dict(document)
        if embeddings is not None:
            payload["encoded_content"] = embeddings.tolist()

        kwargs: dict[str, Any] = {"index": index_name, "body": payload}
        if doc_id is not None:
            kwargs["id"] = doc_id
        return dict(self.client.index(**kwargs))

    def bulk_index_documents(
        self,
        index_name: str,
        documents: list[dict[str, Any]],
        doc_id_field: str | None = None,
    ) -> dict[str, Any]:
        actions = []
        for doc in documents:
            action: dict[str, Any] = {"_index": index_name, "_source": doc}
            if doc_id_field and doc_id_field in doc:
                action["_id"] = doc[doc_id_field]
            actions.append(action)

        success_count, failed_items = bulk(self.client, actions, stats_only=False)
        return {
            "success_count": success_count,
            "failed_count": len(failed_items),
            "failed_items": failed_items,
        }

    def get_document(self, index_name: str, doc_id: str) -> dict[str, Any] | None:
        response = self.client.get(index=index_name, id=doc_id)
        return response.get("_source") if response.get("found") else None

    def update_document(self, index_name: str, doc_id: str, update_doc: dict[str, Any]) -> dict[str, Any]:
        return dict(self.client.update(index=index_name, id=doc_id, body={"doc": update_doc}))

    def delete_document(self, index_name: str, doc_id: str) -> bool:
        response = self.client.delete(index=index_name, id=doc_id)
        return response.get("result") == "deleted"

    def search_documents(
        self,
        index_name: str,
        query: dict[str, Any],
        size: int = 10,
        from_: int = 0,
    ) -> dict[str, Any]:
        return dict(self.client.search(index=index_name, body={"query": query}, size=size, from_=from_))

    def simple_search(
        self,
        index_name: str,
        search_text: str,
        fields: list[str] | None = None,
        size: int = 10,
        from_: int = 0,
    ) -> list[dict[str, Any]]:
        query = (
            {"multi_match": {"query": search_text, "fields": fields}}
            if fields
            else {"query_string": {"query": search_text}}
        )
        response = self.search_documents(index_name, query, size=size, from_=from_)
        return [hit["_source"] for hit in response.get("hits", {}).get("hits", [])]

    def count_documents(self, index_name: str, query: dict[str, Any] | None = None) -> int:
        response = self.client.count(index=index_name, body={"query": query} if query else None)
        return int(response.get("count", 0))

    def refresh_index(self, index_name: str) -> bool:
        response = self.client.indices.refresh(index=index_name)
        return not response.get("_shards", {}).get("failed", 0)



