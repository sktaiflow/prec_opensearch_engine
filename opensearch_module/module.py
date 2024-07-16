from time import time
import logging
from opensearchpy import helpers, OpenSearch
from datetime import datetime

from utils.dec
from dags.onemodelV3.logging import loguru_logger


from utils.decorator.exception_handler import exception_handle_operation
from utils.enum import INTERNAL_ERROR_CODES

import traceback
from pydantic import BaseModel, ValidationError
from functools import wraps
from typing import Callable, Any, Dict, Optional
from opensearch_module.opensearch_schema import ClientSetting

@exception_handle_operation(INTERNAL_ERROR_CODES.DELETE_DOCUMENT_ERROR)
def delete_documents(client, index_name, doc_id, logger):
    logger.info(f"Deleting document {doc_id} from index {index_name}")
    return client.delete(index=index_name, id=doc_id)
    

@exception_handle_operation(INTERNAL_ERROR_CODES.UPDATE_DOCUMENT_ERROR)
def update_documents(client, index_name, doc_id, doc_body, logger):
    update_body = {
        "doc": doc_body,
        "doc_as_upsert": True
    }
    logger.info(f"Updating document {doc_id} in index {index_name}")
    return client.update(index=index_name, id=doc_id, body=update_body)

@exception_handle_operation(INTERNAL_ERROR_CODES.CREATE_CLIENT_ERROR)
def create_client(client_setting:ClientSetting,  logger, **kwargs):        
    return OpenSearch(
        hosts = [{"host": client_setting.host, "port": client_setting.port}],
        http_compress=client_setting.http_compress,
        use_ssl=client_setting.use_ssl,
        verify_certs=client_setting.verify_certs,
        timeout=client_setting.timeout,
        pool_maxsize=client_setting.pool_maxsize,
        http_auth=client_setting.http_auth
    )

@exception_handle_operation
def create_index(client, index_name, index_body, logger):
    """ 신규 인덱스를 생성 """
    return client.indices.create(index=index_name, body=index_body)

@exception_handle_operation(INTERNAL_ERROR_CODES.DELETE_INDEX_ERROR)
def remove_index(client, index_name, logger):
    """인덱스를 삭제한다"""
    logger.info(f"[remove_index] remove_index {index_name}")
    return client.indices.delete(index=index_name)  
        
def index_check(client, index_name):
    return client.indices.exists(index_name)

@exception_handle_operation(INTERNAL_ERROR_CODES.INDEXING_ERROR)
def indexing_data(client, generator, logger, **kwargs):
    """ data indexing """
    return helpers.bulk(
        client, generator, chunk_size=kwargs.get('chunk_size', 100), request_timeout=kwargs.get('chunk_size', 300)
    )


def analyze_query(client, index_name, query, analyzer:str=None):
    if analyzer is None:
        analyzer = 'standard'
    
    body =  {
        "analyzer": analyzer,
        "text": query
    }

    response = client.indices.analyze(
        index=index_name,
        body=body
    )
    return response