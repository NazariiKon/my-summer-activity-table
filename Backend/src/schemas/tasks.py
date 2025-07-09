from pydantic import BaseModel

class TaskSchema(BaseModel):
    description: str
    completed: bool
    day_id: int
    category_id: int

class CategorySchema(BaseModel):
    title: str

class UpdateSchema(BaseModel):
    description: str