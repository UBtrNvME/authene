from contextvars import ContextVar
from os import path
from typing import Final, Optional
from uuid import uuid1

from fastapi import FastAPI, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import scoped_session
from starlette.requests import Request

from authene_common import config
from authene_common.database import engine, sessionmaker


async def not_found(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": [{"msg": "Not Found."}]},
    )


exception_handlers = {404: not_found}

app = FastAPI(exception_handlers=exception_handlers, openapi_url="")

frontend = FastAPI(openapi_url="")


@frontend.middleware("http")
async def default_page(request, call_next):
    response = await call_next(request)
    if response.status_code == 404:
        if config.STATIC_DIR:
            return FileResponse(path.join(config.STATIC_DIR, "index.html"))
    return response


api = FastAPI(
    title="Authene",
    description="Welcome to Authene's API documentation! Here you will able to discover all of the ways you can interact with the Authene API.",
    root_path="/api/v1",
    docs_url=None,
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)


REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())

    # we create a per-request id such that we can ensure that our session is scoped for a particular request.
    # see: https://github.com/tiangolo/fastapi/issues/726
    ctx_token = _request_id_ctx_var.set(request_id)

    try:
        session = scoped_session(sessionmaker(bind=engine), scopefunc=get_request_id)
        request.state.db = session()
        response = await call_next(request)
    except Exception as e:
        raise e from None
    finally:
        request.state.db.close()

    _request_id_ctx_var.reset(ctx_token)
    return response


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=31536000 ; includeSubDomains"
    return response


api.include_router(api_router)


# we mount the frontend and app
if config.STATIC_DIR and path.isdir(config.STATIC_DIR):
    frontend.mount("/", StaticFiles(directory=config.STATIC_DIR), name="app")

app.mount("/api/v1", app=api)
app.mount("/", app=frontend)
