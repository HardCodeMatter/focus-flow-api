from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from service import BaseService

from .models import Task
from .repository import TaskRepository
from .schemas import TaskCreate, TaskRead, TaskUpdate


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
                detail='Task is not found',
            )
        
        return await self.repository.get_by_id(id)
    
    async def get_all(self) -> list[Task]:
        return await self.repository.get_all()
    
    async def update(self, id: str, task_data: TaskUpdate) -> Task:
        if not await self.repository.task_exists_by_id(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.',
            )
        
        task: Task = await self.repository.get_by_id(id)

        return await self.repository.update(task, task_data)
    
    async def delete(self, id: str) -> bool:
        if not await self.repository.task_exists_by_id(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.'
            )
        
        task: Task = await self.repository.get_by_id(id)
        await self.repository.delete(task)

        return True
