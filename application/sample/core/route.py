from fastapi import APIRouter

from core.depends import DependsAppState, DependsDatabase, DependsAsyncTransactionalSession

router = APIRouter(
    prefix="/sample/core",
    tags=["/sample/core"]
)


@router.get('/app_state')
async def get_app_state(app_state: DependsAppState):
    return f'{repr(app_state)} {id(app_state)}'


@router.get('/app_state_2')
async def get_app_state2(app_state: DependsAppState):
    return f'{repr(app_state)} {id(app_state)}'


@router.get('/database')
async def get_database(database : DependsDatabase):
    return f'{repr(database)} {id(database)}'


@router.get('/database_2')
async def get_database2(database: DependsDatabase):
    return f'{repr(database)} {id(database)}'


@router.get('/session')
async def get_session(session: DependsAsyncTransactionalSession):
    return f'{repr(session)} {id(session)}'
