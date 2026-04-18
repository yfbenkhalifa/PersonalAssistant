# Elasticsearch Stack (Dev)

Local 3-node Elasticsearch cluster + Kibana for development.

## Usage

```bash
cp .env.example .env          # edit passwords
docker compose up -d
```

Kibana will be available at http://localhost:${KIBANA_PORT:-5601} and
Elasticsearch at https://localhost:${ES_PORT:-9200}.

Stop and remove volumes:

```bash
docker compose down -v
```

