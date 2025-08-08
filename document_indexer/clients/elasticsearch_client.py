
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from typing import List, Dict, Any, Optional, Union
from loguru import logger
import numpy as np


class ElasticSearchClient:
    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        """
        Initialize the Elasticsearch client.
        
        :param host: Elasticsearch host URL (e.g., 'localhost:9200' or 'https://es-cluster:9200')
        """
        self.client = Elasticsearch(f"{host}:{port}", basic_auth=(user, password))
        
        self.host = host
        self.port = port
        self.user = user

    def health_check(self) -> bool:
        """
        Check if Elasticsearch cluster is healthy and reachable.
        
        :return: True if healthy, False otherwise
        """
        try:
            health = self.client.cluster.health()
            return health['status'] in ['green', 'yellow']
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def create_index(self, index_name: str, mapping: Optional[Dict] = None, settings: Optional[Dict] = None) -> bool:
        """
        Create an index with optional mapping and settings.
        
        :param index_name: Name of the index to create
        :param mapping: Index mapping configuration
        :param settings: Index settings configuration
        :return: True if created successfully, False otherwise
        """
        try:
            body = {}
            if mapping:
                body['mappings'] = mapping
            if settings:
                body['settings'] = settings
                
            response = self.client.indices.create(index=index_name)
            logger.info(f"Index '{index_name}' created successfully")
            return response.get('acknowledged', False)
        except Exception as e:
            logger.error(f"Failed to create index '{index_name}': {e}")
            return False

    def index_exists(self, index_name: str) -> bool:
        """
        Check if an index exists.
        
        :param index_name: Name of the index to check
        :return: True if exists, False otherwise
        """
        return self.client.indices.exists(index=index_name)

    def delete_index(self, index_name: str) -> bool:
        """
        Delete an index.
        
        :param index_name: Name of the index to delete
        :return: True if deleted successfully, False otherwise
        """
        try:
            if self.index_exists(index_name):
                response = self.client.indices.delete(index=index_name)
                logger.info(f"Index '{index_name}' deleted successfully")
                return response.get('acknowledged', False)
            return True
        except Exception as e:
            logger.error(f"Failed to delete index '{index_name}': {e}")
            return False

    def index_document(self, index_name: str, document: Dict[str, Any], doc_id: Optional[str] = None, embeddings: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """
        Index a single document in the specified Elasticsearch index.

        :param index_name: Name of the index where the document will be stored
        :param document: The document to be indexed
        :param doc_id: Optional document ID. If not provided, Elasticsearch will generate one
        :return: Response from Elasticsearch after indexing the document
        """
        try:
            kwargs = {'index': index_name, 'body': document}
            if doc_id:
                kwargs['id'] = doc_id
            
            if embeddings is not None:
                if not isinstance(embeddings, np.ndarray):
                    raise ValueError("Embeddings must be a numpy ndarray")
                if embeddings.ndim != 1:
                    raise ValueError("Embeddings must be a 1-dimensional array")
                kwargs['body']['text_embedding_2'] = embeddings.tolist() 
                
            response = self.client.index(**kwargs)
            if response.get('result') not in ['created', 'updated']:
                raise Exception(f"Unexpected result: {response.get('result')}")
            return response
        except Exception as e:
            logger.error(f"Failed to index document in '{index_name}': {e}")
            raise

    def bulk_index_documents(self, index_name: str, documents: List[Dict[str, Any]], doc_id_field: Optional[str] = None) -> Dict[str, Any]:
        """
        Bulk index multiple documents for better performance.
        
        :param index_name: Name of the index where documents will be stored
        :param documents: List of documents to be indexed
        :param doc_id_field: Field name to use as document ID (optional)
        :return: Bulk indexing response summary
        """
        try:
            actions = []
            for doc in documents:
                action = {
                    '_index': index_name,
                    '_source': doc
                }
                if doc_id_field and doc_id_field in doc:
                    action['_id'] = doc[doc_id_field]
                actions.append(action)
            
            success_count, failed_items = bulk(self.client, actions)
            
            result = {
                'success_count': success_count,
                'failed_count': len(failed_items),
                'failed_items': failed_items
            }
            
            if failed_items:
                logger.warning(f"Bulk indexing completed with {len(failed_items)} failures")
            else:
                logger.info(f"Successfully bulk indexed {success_count} documents to '{index_name}'")
                
            return result
        except Exception as e:
            logger.error(f"Failed to bulk index documents to '{index_name}': {e}")
            raise

    def get_document(self, index_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its ID.
        
        :param index_name: Name of the index
        :param doc_id: Document ID
        :return: Document if found, None otherwise
        """
        try:
            response = self.client.get(index=index_name, id=doc_id)
            return response['_source'] if response['found'] else None
        except Exception as e:
            logger.error(f"Failed to get document '{doc_id}' from '{index_name}': {e}")
            return None

    def update_document(self, index_name: str, doc_id: str, update_doc: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a document by its ID.
        
        :param index_name: Name of the index
        :param doc_id: Document ID
        :param update_doc: Fields to update
        :return: Update response
        """
        try:
            response = self.client.update(
                index=index_name,
                id=doc_id,
                body={'doc': update_doc}
            )
            return response
        except Exception as e:
            logger.error(f"Failed to update document '{doc_id}' in '{index_name}': {e}")
            raise

    def delete_document(self, index_name: str, doc_id: str) -> bool:
        """
        Delete a document by its ID.
        
        :param index_name: Name of the index
        :param doc_id: Document ID
        :return: True if deleted successfully, False otherwise
        """
        try:
            response = self.client.delete(index=index_name, id=doc_id)
            return response.get('result') == 'deleted'
        except Exception as e:
            logger.error(f"Failed to delete document '{doc_id}' from '{index_name}': {e}")
            return False

    def search_documents(self, index_name: str, query: Dict[str, Any], size: int = 10, from_: int = 0) -> Dict[str, Any]:
        """
        Search for documents in the index.
        
        :param index_name: Name of the index to search
        :param query: Elasticsearch query DSL
        :param size: Number of results to return
        :param from_: Starting offset for pagination
        :return: Search response
        """
        try:
            response = self.client.search(
                index=index_name,
                body={'query': query},
                size=size,
                from_=from_
            )
            return response
        except Exception as e:
            logger.error(f"Failed to search in '{index_name}': {e}")
            raise

    def simple_search(self, index_name: str, search_text: str, fields: List[str] = None, size: int = 10) -> List[Dict[str, Any]]:
        """
        Perform a simple text search across specified fields.
        
        :param index_name: Name of the index to search
        :param search_text: Text to search for
        :param fields: List of fields to search in (searches all fields if None)
        :param size: Number of results to return
        :return: List of matching documents
        """
        try:
            if fields:
                query = {
                    'multi_match': {
                        'query': search_text,
                        'fields': fields
                    }
                }
            else:
                query = {
                    'query_string': {
                        'query': search_text
                    }
                }
            
            response = self.search_documents(index_name, query, size)
            return [hit['_source'] for hit in response['hits']['hits']]
        except Exception as e:
            logger.error(f"Failed to perform simple search in '{index_name}': {e}")
            raise

    def count_documents(self, index_name: str, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents in an index, optionally with a query filter.
        
        :param index_name: Name of the index
        :param query: Optional query to filter documents
        :return: Number of matching documents
        """
        try:
            body = {'query': query} if query else None
            response = self.client.count(index=index_name, body=body)
            return response['count']
        except Exception as e:
            logger.error(f"Failed to count documents in '{index_name}': {e}")
            return 0

    def refresh_index(self, index_name: str) -> bool:
        """
        Refresh an index to make recent changes available for search.
        
        :param index_name: Name of the index to refresh
        :return: True if refreshed successfully, False otherwise
        """
        try:
            response = self.client.indices.refresh(index=index_name)
            return not response.get('_shards', {}).get('failed', 0)
        except Exception as e:
            logger.error(f"Failed to refresh index '{index_name}': {e}")
            return False

