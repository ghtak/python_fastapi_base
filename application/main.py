from fastapi import FastAPI

from application.sample.core.route import router as core_sample_router
from application.user.route import router as user_router
from core.app_state import AppState


def init_route(app_: FastAPI) -> FastAPI:
    app_.include_router(core_sample_router)
    app_.include_router(user_router)
    return app_


def create_app() -> FastAPI:
    app_state = AppState()
    app_state.init_logging()

    app_ = FastAPI()
    app_ = init_route(app_)
    # app_.dependency_overrides[AppState] = lambda: core
    return app_


app = create_app()


@app.get("/")
async def home():
    return "hello fastapi"
