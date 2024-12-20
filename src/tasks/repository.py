from sqlalchemy import Select, select

from repository import BaseRepository

from .models import Task
from .schemas import TaskCreate, TaskRead, TaskUpdate


class TaskRepository(BaseRepository):
    async def create(self, task_data: TaskCreate) -> TaskRead:
        task: Task = Task(**task_data.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return TaskRead(**task.__dict__)
    
    async def get_by_id(self, _id: str) -> Task:
        stmt: Select[Task] = select(Task).filter(Task.id == _id)
        task: Task = (
            await self.session.execute(stmt)
        ).scalar_one_or_none()

        return task
    
    async def get_all(self) -> list[TaskRead]:
        stmt: Select[list[Task]] = select(Task)
        tasks: list[Task] = (
            await self.session.execute(stmt)
        ).scalars().all()
        
        return [TaskRead(**task.__dict__) for task in tasks]
    
    async def task_exists_by_id(self, _id: str) -> bool:
        stmt: Select[Task] = select(Task).filter_by(id=_id)
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
    
    async def update(self, task: Task, task_data: TaskUpdate) -> TaskUpdate:
        for key, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        await self.session.commit()
        await self.session.refresh(task)

        return TaskUpdate(**task.__dict__)
    
    async def delete(self, task: Task) -> bool:
        self.session.delete(task)
        await self.session.commit()

        return True
