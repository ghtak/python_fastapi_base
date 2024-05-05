from typing import Annotated

from fastapi import FastAPI, Depends, APIRouter
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.app_state import AppState
from app.config import Config
from app.route import samples


def enable_custom_exception_handlers(app_: FastAPI):
    # @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exception: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": f"{exception}"},
        )

    # @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exception: Exception):
        return JSONResponse(
            status_code=422,
            content={"message": f"{exception}"},
        )

    app_.add_exception_handler(Exception, global_exception_handler)
    app_.add_exception_handler(RequestValidationError, validation_exception_handler)


def enable_cors(app_: FastAPI, cors_origin: list[str]):
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origin,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routes(app_: FastAPI):
    app_.include_router(samples.router)


def create_app() -> FastAPI:
    app_state = AppState(config=Config.from_env())
    app_state.init_logging()

    app_ = FastAPI()
    app_.dependency_overrides[AppState] = lambda: app_state

    enable_custom_exception_handlers(app_)

    if app_state.config.cors_origin is not None:
        enable_cors(app_, app_state.config.cors_origin)

    init_routes(app_)
    return app_


app = create_app()
