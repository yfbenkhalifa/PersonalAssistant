import sys
import importlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
from fastapi.testclient import TestClient

search_api = importlib.import_module("personal_assistant_elasticsearch.api")
search_settings = importlib.import_module("personal_assistant_elasticsearch.settings")

SearchRuntime = search_api.SearchRuntime
create_app = search_api.create_app
SearchServiceSettings = search_settings.SearchServiceSettings


class StubEsClient:
    def __init__(self):
        self.indices = set()
        self.documents = {}

    def health_check(self):
        return True

    def index_exists(self, index_name):
        return index_name in self.indices

    def create_index(self, index_name, mapping=None, settings=None):
        self.indices.add(index_name)
        return True

    def delete_index(self, index_name):
        self.indices.discard(index_name)
        return True

    def refresh_index(self, index_name):
        return True

    def index_document(self, index_name, document, doc_id=None, embeddings=None):
        doc_id = doc_id or f"doc-{len(self.documents) + 1}"
        self.documents[(index_name, doc_id)] = {**document, "encoded_content": embeddings.tolist() if embeddings is not None else None}
        return {"_id": doc_id, "result": "created"}

    def bulk_index_documents(self, index_name, documents):
        for i, document in enumerate(documents, start=1):
            self.documents[(index_name, f"bulk-{i}")] = document
        return {"success_count": len(documents), "failed_count": 0, "failed_items": []}

    def get_document(self, index_name, doc_id):
        return self.documents.get((index_name, doc_id))

    def update_document(self, index_name, doc_id, update_doc):
        self.documents[(index_name, doc_id)].update(update_doc)
        return {"result": "updated"}

    def delete_document(self, index_name, doc_id):
        return self.documents.pop((index_name, doc_id), None) is not None

    def count_documents(self, index_name):
        return sum(1 for stored_index, _ in self.documents if stored_index == index_name)

    def simple_search(self, index_name, search_text, fields=None, size=10, from_=0):
        values = [doc for (stored_index, _), doc in self.documents.items() if stored_index == index_name and search_text.lower() in doc.get("content", "").lower()]
        return values[from_ : from_ + size]


class StubEncoder:
    def encode(self, content):
        return np.array([float(len(content))])


def make_client():
    runtime = SearchRuntime(
        settings=SearchServiceSettings(),
        client=StubEsClient(),
        text_encoder=StubEncoder(),
    )
    return TestClient(create_app(runtime))


def test_create_index_and_check_existence():
    client = make_client()

    create_response = client.post("/api/indices", json={"index_name": "notes"})
    exists_response = client.get("/api/indices/notes/exists")

    assert create_response.status_code == 200
    assert exists_response.json() == {"index_name": "notes", "exists": True}


def test_index_and_fetch_document():
    client = make_client()
    client.post("/api/indices", json={"index_name": "notes"})

    create_doc = client.post(
        "/api/documents/notes",
        json={"title": "Hello", "content": "search me", "author": "wiz", "tags": ["t1"], "metadata": {}},
    )
    doc_id = create_doc.json()["document_id"]
    fetch_doc = client.get(f"/api/documents/notes/{doc_id}")

    assert create_doc.status_code == 200
    assert fetch_doc.status_code == 200
    assert fetch_doc.json()["document"]["content"] == "search me"


def test_search_returns_matching_documents():
    client = make_client()
    client.post("/api/indices", json={"index_name": "notes"})
    client.post(
        "/api/documents/notes",
        json={"title": "Hello", "content": "alpha beta", "author": None, "tags": [], "metadata": {}},
    )
    client.post(
        "/api/documents/notes",
        json={"title": "Other", "content": "gamma", "author": None, "tags": [], "metadata": {}},
    )

    response = client.post("/api/search/notes", json={"query": "alpha", "size": 10, "from": 0})

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["results"][0]["title"] == "Hello"



