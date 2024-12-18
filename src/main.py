import uvicorn
from fastapi import FastAPI

from config import settings

from tasks.routers import router as task_router


app: FastAPI = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION
)

app.include_router(task_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
