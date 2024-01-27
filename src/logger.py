#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Structured logging
"""

import json
import logging
from datetime import datetime
from logging import Formatter

from starlette.middleware.base import BaseHTTPMiddleware
from constants import LOG_APP_NAME


class JsonFormatter(Formatter):
    """Structured logging - json formatter"""

    def __init__(self, module: str):
        super(JsonFormatter, self).__init__()
        self.module = module

    def format(self, record):
        """sendsible attributes for log records"""
        json_record = {}
        json_record["module"] = self.module
        json_record["message"] = record.getMessage()
        json_record["level"] = record.levelname
        json_record["timestamp"] = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%Sz")
        json_record["function"] = record.funcName
        if "req" in record.__dict__:
            json_record["req"] = record.__dict__["req"]
        if "res" in record.__dict__:
            json_record["res"] = record.__dict__["res"]
        if record.levelno == logging.ERROR and record.exc_info:
            json_record["err"] = self.formatException(record.exc_info)

        return json.dumps(json_record)


def get_logger(name: str):
    """Returns a logger with json formatter - logger factory method"""
    logger_obj = logging.root
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter(name))
    logger_obj.handlers = [handler]
    logger_obj.setLevel(logging.DEBUG)

    logging.getLogger("uvicorn.access").disabled = True

    return logger_obj


class LogMiddleware(BaseHTTPMiddleware):
    """Fast api middleware for request logging"""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        logger.info(
            "Incoming request",
            extra={
                "req": {
                    "method": request.method,
                    "url": str(request.url),
                    "ip": request.client.host,
                },
                "res": {
                    "status_code": response.status_code,
                },
            },
        )
        return response


logger = get_logger(LOG_APP_NAME)
