from fastapi import FastAPI, HTTPException
from enum import IntEnum
from typing import List, Optional
from pydantic import BaseModel, Field

api = FastAPI()


class Priority(IntEnum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


class TodoBase(BaseModel):
    todo_name: str = Field(..., min_length=3, max_length=512, description="Name of the todo")
    todo_description: str = Field(..., description="Description of the todo")
    priority: Priority = Field(default=Priority.LOW, description="Priority of the todo")


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    todo_id: int = Field(..., description="Unique Identifier of todo")


class TodoUpdate(BaseModel):
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description="Name of the todo")
    todo_description: Optional[str] = Field(None, description="Description of the todo")
    priority: Optional[Priority] = Field(None, description="Priority of the todo")


# SAMPLE DATABASE (Pydantic Models)
all_todos = [
    Todo(todo_id=1, todo_name="Sports", todo_description="Go to the gym", priority=Priority.HIGH),
    Todo(todo_id=2, todo_name="Read", todo_description="Read 10 pages", priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name="Shop", todo_description="Go shopping", priority=Priority.LOW),
    Todo(todo_id=4, todo_name="Study", todo_description="Study for exam", priority=Priority.MEDIUM),
    Todo(todo_id=5, todo_name="Meditate", todo_description="Meditate 20 minutes", priority=Priority.LOW),
]


@api.get("/")
def index():
    return {"message": "Hello World"}


@api.get("/todos/{todo_id}", response_model=Todo)
async def get_todo_by_id(todo_id: int):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@api.get("/todos", response_model=List[Todo])
async def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    return all_todos


@api.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate):
    new_id = max(t.todo_id for t in all_todos) + 1
    new_todo = Todo(
        todo_id=new_id,
        todo_name=todo.todo_name,
        todo_description=todo.todo_description,
        priority=todo.priority
    )
    all_todos.append(new_todo)
    return new_todo


@api.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated.todo_name is not None:
                todo.todo_name = updated.todo_name
            if updated.todo_description is not None:
                todo.todo_description = updated.todo_description
            if updated.priority is not None:
                todo.priority = updated.priority
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@api.delete("/todos/{todo_id}", response_model=Todo)
async def delete_todo(todo_id: int):
    for i, todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            return all_todos.pop(i)
    raise HTTPException(status_code=404, detail="Todo not found")
