from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class SearchServiceSettings:
    elasticsearch_host: str = "http://localhost"
    elasticsearch_port: int = 9200
    elasticsearch_username: str = "elastic"
    elasticsearch_password: str | None = None
    elasticsearch_api_key: str | None = None
    api_title: str = "Personal Assistant Elasticsearch API"
    api_description: str = "API for indexing and searching documents in Elasticsearch"
    api_version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8100
    default_search_size: int = 10
    max_search_size: int = 100
    max_document_length: int = 4096
    text_encoder_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    text_encoder_provider: str = "SentenceTransformer"
    chunker_host: str = "http://127.0.0.1"
    chunker_port: int = 25000
    chunker_api_key: str | None = None

    @classmethod
    def from_yaml(cls, file_path: str | os.PathLike[str]) -> "SearchServiceSettings":
        with open(file_path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}

        es = data.get("elasticsearch_settings", {})
        text_encoder = data.get("text_encoder", {})
        chunker = data.get("chunk_agent_model", {})
        return cls(
            elasticsearch_host=es.get("host", cls.elasticsearch_host),
            elasticsearch_port=int(es.get("port", cls.elasticsearch_port)),
            elasticsearch_username=es.get("username", cls.elasticsearch_username),
            elasticsearch_password=os.getenv("ELASTICSEARCH_PASSWORD", es.get("password", "")) or None,
            elasticsearch_api_key=os.getenv("ELASTICSEARCH_API_KEY", es.get("api_key", "")) or None,
            api_title=data.get("api_title", cls.api_title),
            api_description=data.get("api_description", cls.api_description),
            api_version=data.get("api_version", cls.api_version),
            host=data.get("host", os.getenv("HOST", cls.host)),
            port=int(data.get("port", os.getenv("PORT", cls.port))),
            default_search_size=int(data.get("default_search_size", cls.default_search_size)),
            max_search_size=int(data.get("max_search_size", cls.max_search_size)),
            max_document_length=int(data.get("max_document_length", cls.max_document_length)),
            text_encoder_model_name=text_encoder.get("model", cls.text_encoder_model_name),
            text_encoder_provider=text_encoder.get("provider", cls.text_encoder_provider),
            chunker_host=chunker.get("host", cls.chunker_host),
            chunker_port=int(chunker.get("port", cls.chunker_port)),
            chunker_api_key=os.getenv("AGENTIC_DOCUMENT_CHUNKER_API_KEY", chunker.get("api_key", "")) or None,
        )


def default_settings_path() -> Path:
    return Path(__file__).resolve().parents[2] / "settings.example.yaml"



