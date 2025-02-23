import typing

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from tasks.schemas import TaskCreate, TaskRead, TaskUpdate, TaskQueryParams, TagCreate, TagRead, TagUpdate
from tasks.service import TaskService, TagService
from users.utils import get_current_user, get_current_active_user

if typing.TYPE_CHECKING:
    from tasks.models import User


router: APIRouter = APIRouter()


@router.post('/tasks', status_code=201, tags=['Tasks'])
async def create_task(
    task_data: TaskCreate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).create(task_data, owner_id=current_user.id)


@router.get('/tasks/{task_id}', status_code=200, tags=['Tasks'])
async def get_task_by_id(
    task_id: str,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).get_by_id(task_id, owner_id=current_user.id)


@router.get('/tasks', status_code=200, tags=['Tasks'])
async def get_tasks(
    params: TaskQueryParams = Depends(),
    page: int = 1,
    limit: int = 10,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[TaskRead]:
    return await TaskService(session).get_all(page, limit, params, owner_id=current_user.id)


@router.patch('/tasks/{task_id}/update', status_code=200, tags=['Tasks'])
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).update(task_id, task_data, owner_id=current_user.id)


@router.delete('/tasks/{task_id}/delete', status_code=200, tags=['Tasks'])
async def delete_task(
    task_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TaskService(session).delete(task_id, owner_id=current_user.id)


@router.post('/tasks/{task_id}/tags', status_code=200, tags=['Tasks'])
async def add_tag(
    task_id: str,
    tag_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TaskService(session).add_tag(task_id, tag_id, owner_id=current_user.id)


@router.delete('/tasks/{task_id}/tags', status_code=200, tags=['Tasks'])
async def remove_tag(
    task_id: str,
    tag_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TaskService(session).remove_tag(task_id, tag_id, owner_id=current_user.id)


@router.post('/tags', status_code=201, tags=['Tags'])
async def create_tag(
    tag_data: TagCreate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).create(tag_data, owner_id=current_user.id)


@router.get('/tags/{tag_id}', status_code=200, tags=['Tags'])
async def get_tag_by_id(
    tag_id: str,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).get_by_id(tag_id, owner_id=current_user.id)


@router.get('/tags', status_code=200, tags=['Tags'])
async def get_tags(
    page: int = 1,
    limit: int = 5,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[TagRead]:
    return await TagService(session).get_all(page, limit, owner_id=current_user.id)


@router.patch('/tags/{tag_id}/update', status_code=200, tags=['Tags'])
async def update_tag(
    tag_id: str,
    tag_data: TagUpdate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).update(tag_id, tag_data, owner_id=current_user.id)


@router.delete('/tags/{tag_id}/delete', status_code=200, tags=['Tags'])
async def delete_tag(
    tag_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TagService(session).delete(tag_id, owner_id=current_user.id)
