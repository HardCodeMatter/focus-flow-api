from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .schemas import TaskCreate, TaskRead, TaskUpdate
from .service import TaskService


router: APIRouter = APIRouter(
    tags=['Tasks'],
)


@router.post('/tasks', status_code=201)
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).create(task_data)


@router.get('/tasks/{id}', status_code=200)
async def get_task_by_id(
    id: str,
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).get_by_id(id)


@router.get('/tasks', status_code=200)
async def get_tasks(session: AsyncSession = Depends(get_async_session)) -> list[TaskRead]:
    return await TaskService(session).get_all()


@router.patch('/tasks/{id}/update', status_code=200)
async def update_task(
    id: str,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> TaskUpdate:
    return await TaskService(session).update(id, task_data)


@router.delete('/tasks/{id}/delete', status_code=200)
async def delete_task(
    id: str,
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TaskService(session).delete(id)
