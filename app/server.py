import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import config


def except_handlers(app_: FastAPI) -> FastAPI:
    async def global_exception_handler(request: Request, exception: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": f"{exception}"},
        )

    async def validation_exception_handler(request: Request, exception: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"message": f"{exception}"},
        )

    app_.add_exception_handler(Exception, global_exception_handler)
    app_.add_exception_handler(RequestValidationError, validation_exception_handler)
    return app_


def enable_cors(app_: FastAPI) -> FastAPI:
    if config.cors_origin is not None:
        app_.add_middleware(
            CORSMiddleware,
            allow_origins=config.cors_origin,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    return app_


def create_app() -> FastAPI:
    logging.basicConfig(
        level=logging.getLevelName(config.log_level),
        datefmt='%Y/%m/%d %H:%M:%S',
        format='%(asctime)s|%(levelname)s|%(message)s',
    )
    app_ = FastAPI()
    app_ = enable_cors(app_)
    app_ = except_handlers(app_)
    return app_


app = create_app()


@app.get("/")
def root():
    return {"Hello": "World"}
