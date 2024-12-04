from fastapi import HTTPException, status

from service import BaseService

from .repository import TaskRepository
from .schemas import TaskCreate, TaskRead, TaskUpdate


class TaskService(BaseService):
    def __init__(self) -> None:
        super.__init__()
        self.repository = TaskRepository(self.session)

    async def create(self, task_data: TaskCreate) -> TaskRead:
        return await self.repository.create(task_data)
    
    async def get_by_id(self, _id: str) -> TaskRead:
        if not await self.repository.task_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found',
            )
        
        return await self.repository.get_by_id(_id)
    
    async def get_all(self) -> list[TaskRead]:
        return await self.repository.get_all()
    
    async def update(self, _id: str, task_data: TaskUpdate) -> TaskRead:
        if not await self.repository.task_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.',
            )
        
        task: TaskRead = await self.repository.get_by_id(_id)

        return await self.repository.update(task, task_data)
    
    async def delete(self, _id: str) -> bool:
        if not await self.repository.task_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.'
            )
        
        task: TaskRead = await self.repository.get_by_id(_id)
        await self.repository.delete(task)

        return True
