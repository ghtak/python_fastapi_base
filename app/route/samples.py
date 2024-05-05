from typing import Annotated

from fastapi import APIRouter, Depends

from app.app_state import AppState

router = APIRouter(
    prefix="/sample",
    tags=["sample"]
)


@router.get("/")
async def home():
    return {"Hello": "World"}


@router.get("/app_state")
async def app_state_depend(app_state: Annotated[AppState, Depends()]):
    return {
        "app_state": str(app_state)
    }
