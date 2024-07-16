import sys
import logging

from datetime import datetime
from types import TracebackType
from typing import Optional, Tuple, Union

from configs import config
from utils import json
from utils.timezone import KST

from app.middlewares import get_request_context

_SysExcInfoType = Union[Tuple[type, BaseException, Optional[TracebackType]], Tuple[None, None, None]]
_ExcInfoType = Union[None, bool, _SysExcInfoType, BaseException]

BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}


class AppLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        extra = {attr: record.__dict__[attr] for attr in record.__dict__ if attr not in BUILTIN_ATTRS}

        if "type" not in extra:
            extra["type"] = "message"

        log = {
            "level": record.levelname,
            "app": config.app_name,
            "version": config.app_version,
            "datetime": datetime.now(KST).isoformat("T"),
            **extra,
        }

        if message := record.getMessage():
            log["message"] = message

        if record.exc_info:
            log["error"] = self.formatException(record.exc_info)

        return json.dumps(log, default=str)


logging.getLogger("opentelemetry").setLevel(logging.CRITICAL)
logging.getLogger("opentelemetry.sdk").setLevel(logging.CRITICAL)
logging.getLogger("opentelemetry.exporter").setLevel(logging.CRITICAL)

logger = logging.getLogger("app")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(AppLogFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def info(
    message: str = "", exc_info: _ExcInfoType = None, stack_info: bool = False, stacklevel: int = 1, **extra
) -> None:
    if "request_id" not in extra:
        request = get_request_context()
        extra["request_id"] = request.state.request_id if request else "-"
    logger.info(message, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)


def warn(
    message: str = "", exc_info: _ExcInfoType = None, stack_info: bool = False, stacklevel: int = 1, **extra
) -> None:
    if "request_id" not in extra:
        request = get_request_context()
        extra["request_id"] = request.state.request_id if request else "-"
    logger.warning(message, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)


def error(
    message: str = "", exc_info: _ExcInfoType = None, stack_info: bool = False, stacklevel: int = 1, **extra
) -> None:
    if "request_id" not in extra:
        request = get_request_context()
        extra["request_id"] = request.state.request_id if request else "-"
    logger.error(message, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)


def exception(
    message: str = "", exc_info: _ExcInfoType = True, stack_info: bool = False, stacklevel: int = 1, **extra
) -> None:
    if "request_id" not in extra:
        request = get_request_context()
        extra["request_id"] = request.state.request_id if request else "-"
    logger.exception(message, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)