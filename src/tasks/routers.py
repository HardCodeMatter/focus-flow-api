from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .schemas import TaskCreate, TaskRead, TaskUpdate, TaskQueryParams, TagCreate, TagRead, TagUpdate
from .service import TaskService, TagService


router: APIRouter = APIRouter()


@router.post('/tasks', status_code=201, tags=['Tasks'])
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).create(task_data)


@router.get('/tasks/{id}', status_code=200, tags=['Tasks'])
async def get_task_by_id(
    id: str,
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).get_by_id(id)


@router.get('/tasks', status_code=200, tags=['Tasks'])
async def get_tasks(
    params: TaskQueryParams = Depends(),
    page: int = 1,
    limit: int = 10,
    session: AsyncSession = Depends(get_async_session)
) -> list[TaskRead]:
    return await TaskService(session).get_all(page, limit, params)


@router.patch('/tasks/{id}/update', status_code=200, tags=['Tasks'])
async def update_task(
    id: str,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).update(id, task_data)


@router.delete('/tasks/{id}/delete', status_code=200, tags=['Tasks'])
async def delete_task(
    id: str,
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TaskService(session).delete(id)


@router.post('/tags', status_code=201, tags=['Tags'])
async def create_tag(
    tag_data: TagCreate,
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).create(tag_data)


@router.get('/tags/{id}', status_code=200, tags=['Tags'])
async def get_tag_by_id(
    id: str,
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).get_by_id(id)


@router.get('/tags', status_code=200, tags=['Tags'])
async def get_tags(
    page: int = 1,
    limit: int = 5,
    session: AsyncSession = Depends(get_async_session)
) -> list[TagRead]:
    return await TagService(session).get_all(page, limit)


@router.patch('/tags/{id}/update', status_code=200, tags=['Tags'])
async def update_tag(
    id: str,
    tag_data: TagUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).update(id, tag_data)


@router.delete('/tags/{id}/delete', status_code=200, tags=['Tags'])
async def delete_tag(
    id: str,
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TagService(session).delete(id)
