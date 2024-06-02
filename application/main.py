from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from application.sample.core.route import router as core_sample_router
from application.user.route import router as user_router
from core.app_context import AppContext
from core.config import Config
from core.database import Database


def init_route(app_: FastAPI) -> FastAPI:
    app_.include_router(core_sample_router)
    app_.include_router(user_router)
    return app_


def enable_custom_exception_handlers(app_: FastAPI) -> FastAPI:
    # @_app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exception: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": f"{exception}"},
        )

    # @_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exception: Exception):
        return JSONResponse(
            status_code=422,
            content={"message": f"{exception}"},
        )

    app_.add_exception_handler(Exception, global_exception_handler)
    app_.add_exception_handler(RequestValidationError, validation_exception_handler)
    return app_


def enable_cors(app_: FastAPI, cors_origin: list[str]) -> FastAPI:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origin,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app_


def create_app() -> FastAPI:
    AppContext.init_logging()
    # AppContext.logger.debug(AppContext.config)

    Database.init(AppContext.config)

    app_ = FastAPI()

    config = Config.from_env()
    if config.cors_origin is not None:
        app_ = enable_cors(app_, config.cors_origin)

    app_ = enable_custom_exception_handlers(app_)
    app_ = init_route(app_)
    # app_.dependency_overrides[AppState] = lambda: app_state
    return app_


app = create_app()


@app.get("/")
async def home():
    return "hello fastapi"
