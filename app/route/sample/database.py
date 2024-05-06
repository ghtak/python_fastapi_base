from typing import Optional, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import entity
from app.database import AsyncScopedSessionDepends, get_scoped_session, DatabaseDepends
from app.repository.user_repository import UserRepository

router = APIRouter(
    prefix="/sample/database",
    tags=["sample_database"]
)


@router.get("/user/{user_id:int}",
            response_model=Optional[entity.User])
async def get_user(
        user_id: int,
        session: AsyncScopedSessionDepends
):
    user_repo = UserRepository(session)
    return await user_repo.get_by_id(user_id)
