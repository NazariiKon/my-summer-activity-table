from fastapi import APIRouter
from src.api.tasks import router as tasks_router
from src.api.init_db import router as database_router

main_router = APIRouter()

main_router.include_router(tasks_router)
main_router.include_router(database_router)