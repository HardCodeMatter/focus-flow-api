from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.elements import UnaryExpression

from repository import BaseRepository
from .models import Task, Tag
from .schemas import TaskCreate, TaskUpdate, TagCreate, TagUpdate


class TaskRepository(BaseRepository):
    async def create(self, task_data: TaskCreate) -> Task:
        task: Task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
        )
        
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task, ['related_tags'])

        return task
    
    async def get_by_id(self, id: str) -> Task:
        stmt: Select[Task] = select(Task).filter_by(id=id).options(selectinload(Task.related_tags))
        task: Task = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return task
    
    async def get_all(self, page: int, limit: int, sort_by: str, order: UnaryExpression) -> list[Task]:
        stmt: Select[list[Task]] = (
            select(Task)
            .options(selectinload(Task.related_tags))
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
    
    async def add_tag(self, task: Task, tag: Tag) -> bool:
        task.related_tags.append(tag)

        await self.session.commit()

        return True
    
    async def remove_tag(self, task: Task, tag: Tag) -> bool:
        task.related_tags.remove(tag)

        await self.session.commit()
        await self.session.refresh(task, ['related_tags'])

        return True
    
    async def tag_exists_in_task(self, task_id: str, tag: Tag) -> bool:
        stmt: Select[Task] = select(Task).filter(Task.id == task_id, Task.related_tags.contains(tag))
        task: Task = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return task is not None


class TagRepository(BaseRepository):
    async def create(self, tag_data: TagCreate) -> Tag:
        tag: Tag = Tag(**tag_data.model_dump())

        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)

        return tag
    
    async def get_by_id(self, tag_id: str) -> Tag:
        stmt: Select[Tag] = select(Tag).filter_by(id=tag_id)
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

    async def update(self, tag: Tag, tag_data: TagUpdate) -> Tag:
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
