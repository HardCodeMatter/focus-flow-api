from fastapi import HTTPException, status
from sqlalchemy import asc, desc, case
from sqlalchemy.ext.asyncio import AsyncSession

from service import BaseService

from .models import Comment, Task, Tag
from .repository import TaskRepository, TagRepository, CommentRepository
from .schemas import TaskCreate, TaskUpdate, SortBy, Order, TaskQueryParams, TagCreate, TagUpdate, CommentCreate, CommentUpdate


class TaskService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.repository = TaskRepository(self.session)
        self.tag_repository = TagRepository(self.session)

    async def create(self, task_data: TaskCreate, owner_id: str) -> Task:
        return await self.repository.create(task_data, owner_id)
    
    async def get_by_id(self, task_id: str, owner_id: str) -> Task:
        if not await self.repository.task_exists_by_id(task_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.',
            )
        
        return await self.repository.get_by_id(task_id, owner_id)
    
    async def get_all(self, page: int, limit: int, params: TaskQueryParams, owner_id: str) -> list[Task]:
        sort_by_mapping: dict = {
            SortBy.priority: case(
                (Task.priority == 'low', 1),
                (Task.priority == 'medium', 2),
                (Task.priority == 'high', 3),
            ),
            SortBy.created_at: Task.created_at,
            SortBy.status: Task.status,
        }
        order_mapping: dict = {
            Order.asc: asc,
            Order.desc: desc,
        }

        sort_by = sort_by_mapping[params.sort_by]
        order_direction = order_mapping[params.order]

        return await self.repository.get_all(page, limit, sort_by, order_direction, owner_id)
    
    async def update(self, task_id: str, task_data: TaskUpdate, owner_id: str) -> Task:
        if not await self.repository.task_exists_by_id(task_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.',
            )
        
        task: Task = await self.repository.get_by_id(task_id, owner_id)

        return await self.repository.update(task, task_data)
    
    async def delete(self, task_id: str, owner_id: str) -> dict[str, str]:
        if not await self.repository.task_exists_by_id(task_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.'
            )
        
        task: Task = await self.repository.get_by_id(task_id, owner_id)
        await self.repository.delete(task)

        return {
            'detail': 'Task is successful deleted.'
        }
    
    async def add_tag(self, task_id: str, tag_id: str, owner_id: str) -> dict[str, str]:
        if not await self.repository.task_exists_by_id(task_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.'
            )
        
        if not await self.tag_repository.tag_exists_by_id(tag_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tag is not found.'
            )
        
        task: Task = await self.repository.get_by_id(task_id, owner_id)
        tag: Tag = await self.tag_repository.get_by_id(tag_id, owner_id)

        if await self.repository.tag_exists_in_task(task_id, tag):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Tag is already added.'
            )

        await self.repository.add_tag(task, tag)

        return {
            'detail': 'Tag is added successful.'
        }
    
    async def remove_tag(self, task_id: str, tag_id: str, owner_id: str) -> dict:
        if not await self.repository.task_exists_by_id(task_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found.'
            )
        
        if not await self.tag_repository.tag_exists_by_id(tag_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tag is not found.'
            )
        
        task: Task = await self.repository.get_by_id(task_id, owner_id)
        tag: Tag = await self.tag_repository.get_by_id(tag_id, owner_id)

        if not await self.repository.tag_exists_in_task(task_id, tag):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tag is already removed.'
            )
        
        await self.repository.remove_tag(task, tag)

        return {
            'detail': 'Tag is removed successful.'
        }


class TagService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.repository = TagRepository(session)

    async def create(self, tag_data: TagCreate, owner_id: str) -> Tag:
        return await self.repository.create(tag_data, owner_id)
    
    async def get_by_id(self, tag_id: str, owner_id: str) -> Tag:
        if not await self.repository.tag_exists_by_id(tag_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tag is not found.',
            )

        return await self.repository.get_by_id(tag_id, owner_id)

    async def get_all(self, page: int, limit: int, owner_id: str) -> list[Tag]:
        return await self.repository.get_all(page, limit, owner_id)

    async def update(self, tag_id: str, tag_data: TagUpdate, owner_id: str) -> Tag:
        if not await self.repository.tag_exists_by_id(tag_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tag is not found.',
            )
        
        tag: Tag = await self.repository.get_by_id(tag_id, owner_id)

        return await self.repository.update(tag, tag_data)

    async def delete(self, tag_id: str, owner_id: str) -> dict[str, str]:
        if not await self.repository.tag_exists_by_id(tag_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tag is not found.',
            )
        
        tag: Tag = await self.repository.get_by_id(tag_id, owner_id)
        await self.repository.delete(tag)

        return {
            'detail': 'Tag is successful deleted.'
        }
      
      
class CommentService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.repository = CommentRepository(session)
        self.task_repository = TaskRepository(session)

    async def create(self, task_id: str, comment_data: CommentCreate, owner_id: str) -> Comment:
        if not await self.task_repository.task_exists_by_id(task_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task is not found',
            )

        return await self.repository.create(task_id, comment_data, owner_id)

    async def get_by_id(self, comment_id: str, owner_id: str) -> Comment:
        if not await self.repository.comment_exists_by_id(comment_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Comment is not found.'
            )
        
        return await self.repository.get_by_id(comment_id, owner_id)

    async def get_all(self, page: int, limit: int, owner_id: str) -> list[Comment]:
        return await self.repository.get_all(page, limit, owner_id)

    async def update(self, comment_id: str, comment_data: CommentUpdate, owner_id: str) -> Comment:
        if not await self.repository.comment_exists_by_id(comment_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Comment is not found.'
            )
        
        comment: Comment = await self.repository.get_by_id(comment_id, owner_id)
        
        return await self.repository.update(comment, comment_data)

    async def delete(self, comment_id: str, owner_id: str) -> dict:
        if not await self.repository.comment_exists_by_id(comment_id, owner_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Comment is not found.'
            )
        
        comment: Comment = await self.repository.get_by_id(comment_id, owner_id)
        await self.repository.delete(comment)

        return {
            'detail': 'Comment is successful deleted.'
        }
