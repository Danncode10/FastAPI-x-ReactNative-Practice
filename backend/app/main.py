from fastapi import FastAPI

api = FastAPI()

# Sample Database
all_todos = [
    {"todo_id": 1, "todo_name": "Sports", "todo_description": "Go to the gym"},
    {"todo_id": 2, "todo_name": "Read", "todo_description": "Read 10 pages"},
    {"todo_id": 3, "todo_name": "Shop", "todo_description": "Go shopping"},
    {"todo_id": 4, "todo_name": "Study", "todo_description": "Study for exam"},
    {"todo_id": 5, "todo_name": "Meditate", "todo_description": "Meditate 20 minutes"},
]


@api.get("/")
def index():
    return {"message": "Hello World"}

@api.get("/todos")
async def get_todo(first_n: int = None):
    if first_n: #if first_n has value
        return all_todos[:first_n]
    else:
        return all_todos

@api.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for todo in all_todos:
        if todo["todo_id"] == todo_id:
            return {"result": todo}
    return {"error": "Todo not found"}

@api.post("/todos")
async def create_todo(todo: dict):
    new_todo_id = max(t["todo_id"] for t in all_todos) + 1
    new_todo = {
        "todo_id": new_todo_id,
        "todo_name": todo["todo_name"],
        "todo_description": todo["todo_description"]
    }
    all_todos.append(new_todo)
    return {"result": new_todo}

@api.put("/todos/{todo_id}")
async def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo["todo_id"] == todo_id:
            todo["todo_name"] = updated_todo["todo_name"]
            todo["todo_description"] = updated_todo["todo_description"]
            return {"result": todo}
    return {"error": "Todo not found"}

@api.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for index, todo in enumerate(all_todos):
        if todo["todo_id"] == todo_id:
            deleted_todo = all_todos.pop(index)
            return {"result": deleted_todo}
    return {"error": "Todo not found"}

