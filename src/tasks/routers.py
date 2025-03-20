import typing

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from tasks.schemas import TaskCreate, TaskRead, TaskUpdate, TaskQueryParams, TagCreate, TagRead, TagUpdate, CommentCreate, CommentRead, CommentUpdate, ReportCreate, ReportRead
from tasks.service import TaskService, TagService, CommentService, ReportService
from users.utils import get_current_user, get_current_active_user

if typing.TYPE_CHECKING:
    from tasks.models import User


router: APIRouter = APIRouter()


@router.post('/tasks', status_code=201, tags=['Tasks'])
async def create_task(
    task_data: TaskCreate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).create(task_data, owner_id=current_user.id)


@router.get('/tasks/{task_id}', status_code=200, tags=['Tasks'])
async def get_task_by_id(
    task_id: str,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).get_by_id(task_id, owner_id=current_user.id)


@router.get('/tasks', status_code=200, tags=['Tasks'])
async def get_tasks(
    params: TaskQueryParams = Depends(),
    page: int = 1,
    limit: int = 10,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[TaskRead]:
    return await TaskService(session).get_all(page, limit, params, owner_id=current_user.id)


@router.patch('/tasks/{task_id}/update', status_code=200, tags=['Tasks'])
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> TaskRead:
    return await TaskService(session).update(task_id, task_data, owner_id=current_user.id)


@router.delete('/tasks/{task_id}/delete', status_code=200, tags=['Tasks'])
async def delete_task(
    task_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TaskService(session).delete(task_id, owner_id=current_user.id)

  
@router.post('/tasks/{task_id}/tags', status_code=200, tags=['Tasks'])
async def add_tag(
    task_id: str,
    tag_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TaskService(session).add_tag(task_id, tag_id, owner_id=current_user.id)


@router.delete('/tasks/{task_id}/tags', status_code=200, tags=['Tasks'])
async def remove_tag(
    task_id: str,
    tag_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TaskService(session).remove_tag(task_id, tag_id, owner_id=current_user.id)


@router.post('/tags', status_code=201, tags=['Tags'])
async def create_tag(
    tag_data: TagCreate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).create(tag_data, owner_id=current_user.id)


@router.get('/tags/{tag_id}', status_code=200, tags=['Tags'])
async def get_tag_by_id(
    tag_id: str,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).get_by_id(tag_id, owner_id=current_user.id)


@router.get('/tags', status_code=200, tags=['Tags'])
async def get_tags(
    page: int = 1,
    limit: int = 5,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[TagRead]:
    return await TagService(session).get_all(page, limit, owner_id=current_user.id)


@router.patch('/tags/{tag_id}/update', status_code=200, tags=['Tags'])
async def update_tag(
    tag_id: str,
    tag_data: TagUpdate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> TagRead:
    return await TagService(session).update(tag_id, tag_data, owner_id=current_user.id)


@router.delete('/tags/{tag_id}/delete', status_code=200, tags=['Tags'])
async def delete_tag(
    tag_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await TagService(session).delete(tag_id, owner_id=current_user.id)


@router.post('/comments', status_code=201, tags=['Comments'])
async def create_comment(
    task_id: str,
    comment_data: CommentCreate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> CommentRead:
    return await CommentService(session).create(task_id, comment_data, owner_id=current_user.id)


@router.get('/comments/{comment_id}', status_code=200, tags=['Comments'])
async def get_comment_by_id(
    comment_id: str,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> CommentRead:
    return await CommentService(session).get_by_id(comment_id, owner_id=current_user.id)


@router.get('/comments', status_code=200, tags=['Comments'])
async def get_comments(
    page: int = 1,
    limit: int = 10,
    current_user: 'User' = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[CommentRead]:
    return await CommentService(session).get_all(page, limit, owner_id=current_user.id)


@router.patch('/comments/{comment_id}/update', status_code=200, tags=['Comments'])
async def update_comment(
    comment_id: str,
    comment_data: CommentUpdate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> CommentRead:
    return await CommentService(session).update(comment_id, comment_data, owner_id=current_user.id)


@router.delete('/comments/{comment_id}/delete', status_code=200, tags=['Comments'])
async def delete_comment(
    comment_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await CommentService(session).delete(comment_id, owner_id=current_user.id)


@router.post('/reports', status_code=201, tags=['Reports'])
async def create_report(
    report_data: ReportCreate,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> ReportRead:
    return await ReportService(session).create(report_data, owner_id=current_user.id)


@router.get('/reports/{report_id}', status_code=200, tags=['Reports'])
async def get_report_by_id(
    report_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> ReportRead:
    return await ReportService(session).get_by_id(report_id, owner_id=current_user.id)


@router.get('/reports', status_code=200, tags=['Reports'])
async def get_reports(
    page: int = 1,
    limit: int = 5,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> list[ReportRead]:
    return await ReportService(session).get_all(page, limit, owner_id=current_user.id)


@router.delete('/reports/{report_id}/delete', status_code=200, tags=['Reports'])
async def delete_report(
    report_id: str,
    current_user: 'User' = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await ReportService(session).delete(report_id, owner_id=current_user.id)
