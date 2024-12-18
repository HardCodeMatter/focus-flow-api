from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from .schemas import TaskCreate, TaskRead, TaskUpdate
from .service import TaskService


router: APIRouter = APIRouter(
    tags=['Tasks'],
)


@router.post('/tasks')
async def create_task(
    task_data: TaskCreate,
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).create(task_data)


@router.get('/tasks/{_id}')
async def get_task_by_id(
    _id: str,
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).get_by_id(_id)


@router.get('/tasks')
async def get_tasks(session: AsyncSession = Depends(get_async_session)) -> list[TaskRead]:
    return await TaskService(session).get_all()


@router.patch('/tasks/{_id}/update')
async def update_task(
    _id: str,
    task_data: TaskUpdate,
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).update(_id, task_data)
