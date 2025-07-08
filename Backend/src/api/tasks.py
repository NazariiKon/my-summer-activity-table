from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from datetime import date, timedelta

from src.api.dependencies import SessionDep
from src.database import Base, engine
from src.models.tasks import CategoryModel, DayModel, TaskModel
from src.schemas.tasks import TaskSchema, CategorySchema

router = APIRouter()

@router.get("/tasks", tags=["Tasks"], summary="Get all tasks")
async def read_tasks(session: SessionDep):
    query = select(TaskModel)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/task/{task_id}", tags=["Tasks"], summary="Get a book by ID")
async def get_task(task_id: int, session: SessionDep):
    query = select(TaskModel).where(TaskModel.id == task_id)
    result = await session.execute(query)
    task = result.scalars().first()
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail="This task doesn't exist")

@router.get("/task/{day_id}", tags=["Tasks"], summary="Get tasks by day")
async def get_task(day_id: int, session: SessionDep):
    query = select(TaskModel).where(TaskModel.day_id == day_id)
    result = await session.execute(query)
    task = result.scalars().all()
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail="This task doesn't exist")

@router.post("/tasks/", tags=["Tasks"], summary="Create a new task")
async def create_task(data: TaskSchema, session: SessionDep):
    new_task = TaskModel(
        description = data.description,
        completed = data.completed,
        day_id = data.day_id,
        category_id = data.category_id
    )
    session.add(new_task)
    await session.commit()
    return {"success": True, "message": "The task was created successfully"}



@router.get("/category/", tags=["Category"], summary="Get categories")
async def read_tasks(session: SessionDep):
    query = select(CategoryModel)
    result = await session.execute(query)
    return result.scalars().all()

@router.post("/category/", tags=["Category"], summary="Create a new category")
async def create_category(data: CategorySchema, session: SessionDep):
    new_category = CategoryModel(
        title = data.title
    )
    session.add(new_category)
    await session.commit()
    return {"success": True, "message": "The category was created successfully"}

@router.get("/day/", tags=["Day"], summary="Get days")
async def read_days(session: SessionDep):
    query = select(DayModel).where(DayModel.date <= date.today())
    result = await session.execute(query)
    return result.scalars().all()[::-1]