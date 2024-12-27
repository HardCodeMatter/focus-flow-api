from fastapi import HTTPException, status
from sqlalchemy import asc, desc, case
from sqlalchemy.ext.asyncio import AsyncSession

from service import BaseService

from .models import Task
from .repository import TaskRepository
from .schemas import TaskCreate, TaskUpdate, SortBy, Order, TaskQueryParams


class TaskService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.repository = TaskRepository(self.session)

    async def create(self, task_data: TaskCreate) -> Task:
        return await self.repository.create(task_data)
    
    async def get_by_id(self, id: str) -> Task:
        if not await self.repository.task_exists_by_id(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.',
            )
        
        return await self.repository.get_by_id(id)
    
    async def get_all(self, page: int, limit: int, params: TaskQueryParams) -> list[Task]:
        sort_by_mapping: dict = {
            SortBy.priority: case(
                (Task.priority == 'low', 1),
                (Task.priority == 'medium', 2),
                (Task.priority == 'high', 3),
            ),
            SortBy.created_at: Task.created_at,
            SortBy.is_completed: Task.is_completed,
        }
        order_mapping: dict = {
            Order.asc: asc,
            Order.desc: desc,
        }

        sort_by = sort_by_mapping[params.sort_by]
        order_direction = order_mapping[params.order]

        return await self.repository.get_all(page, limit, sort_by, order_direction)
    
    async def update(self, id: str, task_data: TaskUpdate) -> Task:
        if not await self.repository.task_exists_by_id(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.',
            )
        
        task: Task = await self.repository.get_by_id(id)

        return await self.repository.update(task, task_data)
    
    async def delete(self, id: str) -> dict[str, str]:
        if not await self.repository.task_exists_by_id(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.'
            )
        
        task: Task = await self.repository.get_by_id(id)
        await self.repository.delete(task)

        return {
            'detail': 'Task is successful deleted.'
        }
