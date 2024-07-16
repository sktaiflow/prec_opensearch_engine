from enum import Enum, auto

class StrEnum(str, Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value

    @classmethod
    def list_values(cls) -> list[str]:
        return [e.value for e in cls]

    @classmethod
    def list_names(cls) -> list[str]:
        return [e.name for e in cls]


class GLOBAL_ERROR_CODES(Enum):
    FORBIDDEN = ("403", "[GlobalCode]Forbidden (API 접근권한 미존재)")
    INTERNET_ERROR = ("404", "[GlobalCode]Internet Error (Internet 연결 오류)")
    INVALID_METHOD = ("405", "[GlobalCode]Invalid Method (Request Method <Get, Post> 불일치)")
    INVALID_INPUT_TYPE = ("422", "[GlobalCode]Invalid Input Type (Request Body 내, Input Key 값 오류 혹은 필수 Input Key 값 누락)")
    ENGINE_LOGIC_ERROR = ("444", "[CustomCode]Engine Logic Error (Engine 내부 동작 오류)")
    INTERNET_SERVER_ERROR = ("500", "[GlobalCode]Internet Server Error (Engine Code or Traffic 과부하 오류)")
    ENGINE_SERVER_ERROR = ("445", "[CustomCode]Engine Server Error(Engine 인덱스 업데이트 속도 오류)")
    OPENSEARCH_INDEX_ERROR = ("446", "[CustomCode]Opensearch Index Error(오픈서치 인덱스 오류)")
    OPENSEARCH_ERROR = ("447", "[CustomCode]Opensearch  Error(오픈서치 검색 API 오류)")
    CATEGORY_CLASSIFIER_MODEL_ERROR = ("448", "[CustomCode]Category Classifier model Error(카테고리 모델 오류)")
    MIRRORDB_CONNECTION_ERROR = ("449", "[CustomCode]MirrorDB Connection Error(DB Connection 오류)")
    QUERY_ANALYZER_ERROR = ("450", "[CustomCode]질의분석기 오류")
    GEO_REVERSE_API_ERROR = ("451", "[CustomCode]Geo Reverse API Error(위경도 변환 오류)")

    def __init__(self, code, message):
        self.code = code
        self.message = message


class INTERNAL_ERROR_CODES(StrEnum):
    # Error Codes
    PYDANTIC_VALIDATION_ERROR = "1000"
    CREATE_INDEX_ERROR = "1001"
    DELETE_INDEX_ERROR = "1002"
    INDEXING_ERROR = "1003"
    UPDATE_DOCUMENT_ERROR = "1004"
    DELETE_DOCUMENT_ERROR = "1005"
    SEARCH_ERROR = "1006"
    CREATE_CLIENT_ERROR = "1007"
    INDEX_CHECK = "1008"
    PREPROCESSING_ERROR = "1009"

    # Success Code
    SUCCESS = "200"

    # Warning Code
    INDEX_EXIST = "900"
    
    @classmethod
    def get_message(cls, code, e=''):
        messages = {
            cls.PYDANTIC_VALIDATION_ERROR: f"[ERROR] Pydantic validation check error, detail_message:{e}",
            cls.CREATE_INDEX_ERROR: f"[ERROR] Create index error, detail_message:{e}",
            cls.DELETE_INDEX_ERROR: f"[ERROR] Delete index error, detail_message:{e}",
            cls.INDEXING_ERROR: f"[ERROR] Indexing error, detail_message:{e}",
            cls.UPDATE_DOCUMENT_ERROR: f"[ERROR] Update document error, detail_message:{e}",
            cls.DELETE_DOCUMENT_ERROR: f"[ERROR] Delete document error, detail_message:{e}",
            cls.SEARCH_ERROR: f"[ERROR] Search error, detail_message:{e}",
            cls.INDEX_EXIST: "[WARNING] INDEX EXISTS",
            cls.INDEX_CHECK: "[ERROR] INDEX CHECK FAILED",
            cls.SUCCESS: "SUCCESS",
        }
        return messages.get(code, f"Undefined code, detail_message:{e}")