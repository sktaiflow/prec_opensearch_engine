import os

env = os.environ.get('env', 'stg')

user_dict_package = "" if env == 'prd' else "F73697254"
synonym_dict_package = "" if env == 'prd' else "F246035528"
stopwords_package = "" if env == 'prd' else "F230920579"
updateable = False if env == 'prd' else False

profileIndex_mappings = {
        "properties": {
            "profileId": {"type": "keyword"},
            "svc_mgmt_nums": {"type": "keyword"},
            "lunaIds": {"type": "keyword"},
            "profileText": {"type": "keyword"},
            "source_domain":{"type": "keyword"},
            "created_at": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
            "profileEmbedding": {
                "type": "knn_vector",
                "dimension": 756,
                "method": {
                    "name": "hnsw",
                    "space_type": "l2",
                    "engine": "nmslib",
                    "parameters": {"ef_construction": 16, "m": 16},
                },
            },
        }
    }

common_settings = {
    "index.mapping.ignore_malformed": True,
    "index.search.slowlog.threshold.query.warn": "1s",
    "index": {
        "number_of_shards": 4,
        "number_of_replicas": 1,
        "refresh_interval": "1s",
        "knn": True,
        "analysis":{
            "analyzer": {
                "standard": {
                    "type": "custom",
                    "char_filter":["html_strip"],
                    "tokenizer": "standard_tokenizer",
                    "filter": ["synonyms_filter", "stopwords_filter", "trim", "lowercase"]
                },
                "seunjeon":{
                    "type": "custom",
                    "char_filter":["html_strip"],
                    "tokenizer": "seunjeon_tokenizer",
                    "filter": ["synonyms_filter", "stopwords_filter", "trim", "lowercase"]
                },
                "nori_tokenizer": {
                    "type": "custom",
                    "char_filter":["html_strip"],
                    "tokenizer": "nori_tokenizer",
                    "filter": ["synonyms_filter", "stopwords_filter", "trim", "lowercase", "nori_part_of_speech_filter"]
            }
        },
        "tokenizer":{
            "standard_tokenizer":{
                "type": "standard",
                "user_dictionary": f"analyzers/{user_dict_package}"
            },
            "seunjeon_tokenizer":{
                "type": "seunjeon_tokenizer",
                "user_dictionary": f"analyzers/{user_dict_package}",
                "index_poses":[],
            },
            "nori_tokenizer": {
                "type": "nori_tokenizer",
                "decompound_mode": "mixed",
                "discard_punctuation": True,
                "user_dictionary": f"analyzers/{user_dict_package}"
            },
        },
        "filter": {
            "synonyms_filter":{
                    "type": "synonym",
                    "synonyms_path": f"analyzers/{synonym_dict_package}",
                    "lenient": True,
                    "updateable": updateable
                },  
            "stopwords_filter":{
                "type": "stop",
                "stopwords_path": f"analyzers/{stopwords_package}",
                "lenient": True,
                "updateable": updateable
                },
            "nori_part_of_speech_filter":{
                "type": "nori_part_of_speech",
                "stoptags": [
                    "E", "IC", "J", "MAG", "MAJ",
                    "MM", "SP", "SSC", "SSO", "SC",
                    "SE", "XPN", "XSA", "XSN", "XSV",
                    "UNA", "NA", "VSV"]
            }
        }
    }}
}

profileIndex_body = {
    "settings": common_settings,
    "mappings": profileIndex_mappings
}