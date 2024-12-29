from sqlalchemy import Select, select
from sqlalchemy.sql.elements import UnaryExpression

from repository import BaseRepository

from .models import Task, Tag
from .schemas import TaskCreate, TaskUpdate, TagCreate, TagUpdate


class TaskRepository(BaseRepository):
    async def create(self, task_data: TaskCreate) -> Task:
        task: Task = Task(**task_data.model_dump())
        
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task
    
    async def get_by_id(self, id: str) -> Task:
        stmt: Select[Task] = select(Task).filter_by(id=id)
        task: Task = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return task
    
    async def get_all(self, page: int, limit: int, sort_by: str, order: UnaryExpression) -> list[Task]:
        stmt: Select[list[Task]] = (
            select(Task)
            .order_by(order(sort_by))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        tasks: list[Task] = (
            await self.session.execute(stmt)
        ).scalars().all()
        
        return tasks
    
    async def task_exists_by_id(self, id: str) -> bool:
        stmt: Select[Task] = select(Task).filter_by(id=id)
        task: Task = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return task is not None
    
    async def task_exists_by_title(self, title: str) -> bool:
        stmt: Select[Task] = select(Task).filter_by(title=title)
        task: Task = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return task is not None
    
    async def update(self, task: Task, task_data: TaskUpdate) -> Task:
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)

        return task
    
    async def delete(self, task: Task) -> bool:
        await self.session.delete(task)
        await self.session.commit()

        return True


class TagRepository(BaseRepository):
    async def create(self, tag_data: TagCreate) -> Tag:
        tag: Tag = Tag(**tag_data.model_dump())

        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)

        return tag
    
    async def get_by_id(self, id: str) -> Tag:
        stmt: Select[Tag] = select(Tag).filter_by(id=id)
        tag: Tag = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return tag

    async def get_all(self, page: int, limit: int) -> list[Tag]:
        stmt: Select[list[Tag]] = (
            select(Tag)
            .offset((page - 1) * limit)
            .limit(limit)
        )
        tags: list[Tag] = (
            await self.session.execute(stmt)
        ).scalars().all()

        return tags

    async def update(self, tag: Tag, tag_data: TagCreate) -> Tag:
        for key, value in tag_data.model_dump(exclude_unset=True).items():
            setattr(tag, key, value)

        await self.session.commit()
        await self.session.refresh(tag)

        return tag

    async def delete(self, tag: Tag) -> bool:
        await self.session.delete(tag)
        await self.session.commit()

        return True

    async def tag_exists_by_id(self, id: str) -> bool:
        stmt: Select[Tag] = select(Tag).filter_by(id=id)
        tag: Tag = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return tag is not None
