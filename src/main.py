# -*- coding: utf-8 -*-
"""
API Server for Later service
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# The entire service will be prefixed with /api/v1/later

# from typing import Union

import asyncio
import time
import traceback
from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Request, Response, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

import auth
import config
import constants
import database
import rabbitmq
import redisclient
from logger import logger, LogMiddleware

# import models
from models import request, response
from src.models import basemodel  # @TODO: fix import

REQUEST_TIMEOUT_INTERVAL = 15

settings = config.Config()
match settings.env:
    case "dev":
        logger.info("Running in dev mode")
        app = FastAPI()
    case "stage":
        logger.info("Running in stage mode")
        app = FastAPI()
    case "prod":
        logger.info("Running in prod mode")
        app = FastAPI(docs_url=None, redoc_url=None)  # Disable docs in prod
    case _:
        logger.info("Warning: Running in dev mode")
        app = FastAPI()

app.add_middleware(LogMiddleware)
api_key_header = APIKeyHeader(name="X-API-Key")
db_instance = database.DatabaseFactory(settings)



@app.middleware("http")
async def session_middleware(req: Request, call_next) -> Response:
    """Injects db session into request state and closes it after request is processed"""
    resp = Response('{"status":500,"message":"Internal server error"}', status_code=500, media_type="application/json")
    start_time = time.time()
    try:
        # TODO: Add session pooler
        req.state.db = db_instance.get_session()
        resp = await asyncio.wait_for(call_next(req), REQUEST_TIMEOUT_INTERVAL)
    except asyncio.TimeoutError as e:
        logger.error(f"Request timed out after {duration}s")
        return Response(
            '{"status":504,"message":"Request timed out due to server load"}',
            status_code=504,
            media_type="application/json",
        )
    except Exception as e:
        if settings.debug:
            print(e)
            # print entire traceback

            print(traceback.format_exc())
        else:
            logger.exception(e)
    finally:
        duration = time.time() - start_time
        logger.debug(f"Response time: {duration}")
        logger.debug("Closing db session inside middleware")
        req.state.db.close()
        return resp


def validate_api_key(
    request_api_key: str = Security(api_key_header),
) -> bool:
    """
    Validates if the secret preset in request header X-API-Key matches with the argument secret
    The caller needs to read this secret from the environment variable
    """

    if request_api_key == settings.job_get_api_key:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )




# Dependencies
UserDependancy = Annotated[database.User, Depends(auth.get_current_user)]
DbDepedenancy = Annotated[Session, Depends(database.get_db)]
apikey_dependency = Annotated[bool, Depends(validate_api_key)]


# routes
@app.get("/api/v1/later/")
def root() -> response.ResponseModel:
    """Root path - clone of healthcheck"""
    logger.debug("Health check")
    return response.ResponseModel(
        status=status.HTTP_200_OK,
        message="running",
    )


@app.get("/api/v1/later/health")
def health() -> response.ResponseModel:
    """Provide health check: If service is up and running"""
    logger.debug("Health check")
    return response.ResponseModel(
        status=status.HTTP_200_OK,
        message="running",
    )


@app.get("/api/v1/later", response_model=response.GetJobs, summary="get later items")
def get_later_items(
    current_user: UserDependancy,
    db: DbDepedenancy,
    _: apikey_dependency,
    later_request: request.GetLaterList,
) -> response.GetJobs:
    """
    Get later items
    Needs JWT Auth
    """

    logger.debug(f"Function get_jobs for {current_user.id}")

    jobs_response: List[basemodel.Job] = []
    return response.GetJobs(
        status=status.HTTP_200_OK,
        message="success",
        count=len(jobs_response),
        jobs=jobs_response,
    )

@app.post("/api/v1/later", response_model=response.GetJobs, summary="add something for later")
def add_for_later(
    current_user: UserDependancy,
    db: DbDepedenancy,
    _: apikey_dependency,
    later_request: request.AddForLater,
) -> response.AddForLater:
    """
    Add something for later
    - GenericLink
    - RSSFeed
    - YoutubeVideo
    - TwitterLink
    - GithubRepo
    - GithubGist
    - Note
    - Reminder
    - Image
    - JournalEntry
    Needs JWT Auth
    """

    logger.debug(f"Function get_jobs for {current_user.id}")

    jobs_response: List[basemodel.Job] = []
    return response.GetJobs(
        status=status.HTTP_200_OK,
        message="success",
        count=len(jobs_response),
        jobs=jobs_response,
    )

