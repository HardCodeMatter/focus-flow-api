from sqlalchemy import Select, select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.elements import UnaryExpression

from repository import BaseRepository
from .models import Task, Tag, Comment
from .schemas import TaskCreate, TaskUpdate, TagCreate, TagUpdate, CommentCreate, CommentUpdate


class TaskRepository(BaseRepository):
    async def create(self, task_data: TaskCreate, owner_id: str) -> Task:
        task: Task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
            owner_id=owner_id
        )
        
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task, ['related_tags', 'comments'])

        return task
    
    async def get_by_id(self, task_id: str, owner_id: str) -> Task:
        stmt: Select[Task] = (
            select(Task)
            .filter_by(id=task_id, owner_id=owner_id)
            .options(selectinload(Task.related_tags))
            .options(selectinload(Task.comments))
        )
        task: Task = (
            await self.session.execute(stmt)
        ).scalar_one()

        return task
    
    async def get_all(self, page: int, limit: int, sort_by: str, order: UnaryExpression, owner_id: str) -> list[Task]:
        stmt: Select[list[Task]] = (
            select(Task)
            .filter_by(owner_id=owner_id)
            .options(selectinload(Task.related_tags))
            .options(selectinload(Task.comments))
            .order_by(order(sort_by))
            .offset((page - 1) * limit)
            .limit(limit)
        )
        tasks: list[Task] = (
            await self.session.execute(stmt)
        ).scalars().all()
        
        return tasks
    
    async def task_exists_by_id(self, task_id: str, owner_id: str) -> bool:
        stmt: Select[Task] = select(Task).filter_by(id=task_id, owner_id=owner_id)
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
    async def create(self, tag_data: TagCreate, owner_id: str) -> Tag:
        tag: Tag = Tag(
            **tag_data.model_dump(),
            owner_id=owner_id
        )

        self.session.add(tag)
        await self.session.commit()
        await self.session.refresh(tag)

        return tag
    
    async def get_by_id(self, tag_id: str, owner_id: str) -> Tag:
        stmt: Select[Tag] = select(Tag).filter_by(id=tag_id, owner_id=owner_id)
        tag: Tag = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return tag

    async def get_all(self, page: int, limit: int, owner_id: str) -> list[Tag]:
        stmt: Select[list[Tag]] = (
            select(Tag)
            .filter_by(owner_id=owner_id)
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

    async def tag_exists_by_id(self, tag_id: str, owner_id: str) -> bool:
        stmt: Select[Tag] = select(Tag).filter_by(id=tag_id, owner_id=owner_id)
        tag: Tag = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return tag is not None


class CommentRepository(BaseRepository):
    async def create(self, task_id: str, comment_data: CommentCreate, owner_id: str) -> Comment:
        comment: Comment = Comment(
            **comment_data.model_dump(),
            task_id=task_id,
            owner_id=owner_id
        )

        self.session.add(comment)
        await self.session.commit()
        await self.session.refresh(comment)

        return comment
    
    async def get_by_id(self, comment_id: str, owner_id: str) -> Comment:
        stmt: Select[Comment] = select(Comment).filter_by(id=comment_id, owner_id=owner_id)
        comment: Comment = (
            await self.session.execute(stmt)
        ).scalar_one()

        return comment
    
    async def get_all(self, page: int, limit: int, owner_id: str) -> list[Comment]:
        stmt: Select[list[Comment]] = (
            select(Comment)
            .filter_by(owner_id=owner_id)
            .offset((page - 1) * limit)
            .limit(limit)
        )
        comments: list[Comment] = (
            await self.session.execute(stmt)
        ).scalars().all()

        return comments
    
    async def update(self, comment: Comment, comment_data: CommentUpdate) -> Comment:
        for key, value in comment_data.model_dump(exclude_unset=True).items():
            setattr(comment, key, value)

        await self.session.commit()
        await self.session.refresh(comment)

        return comment
    
    async def delete(self, comment: Comment) -> bool:
        await self.session.delete(comment)
        await self.session.commit()

        return True
    
    async def comment_exists_by_id(self, comment_id: str, owner_id: str) -> bool:
        stmt: Select[Comment] = select(Comment).filter_by(id=comment_id, owner_id=owner_id)
        comment: Comment = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return comment is not None
