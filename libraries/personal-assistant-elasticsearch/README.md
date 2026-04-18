# Personal Assistant Elasticsearch

Standalone Python project for the search and indexing layer extracted from `PersonalAssistant`.

## Included

- `personal_assistant_elasticsearch.clients.ElasticSearchClient`
- `personal_assistant_elasticsearch.document_chunking.DumbDocumentChunker`
- `personal_assistant_elasticsearch.api.create_app()` for a reusable FastAPI service

## Install

```bash
pip install -e .
```

## Run the API locally

```bash
uvicorn personal_assistant_elasticsearch.api:app --reload --port 8100
```

## Example settings

Copy `settings.example.yaml` and adapt it for your environment.

## Test

```bash
pytest
```

