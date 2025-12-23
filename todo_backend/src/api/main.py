from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, database, schemas

app = FastAPI(
    title="Todo Backend API",
    description="RESTful API for managing a simple todo list.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Todos", "description": "CRUD operations for todo items"},
        {"name": "Health", "description": "Health check for service"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for getting DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    """Initialize the database and create tables at startup."""
    database.create_db_and_tables()

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint to confirm the API is running."""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get("/todos", response_model=list[schemas.TodoOut], tags=["Todos"], summary="List all todos")
def list_todos(db: Session = Depends(get_db)):
    """Get a list of all todo items."""
    todos = db.query(models.Todo).all()
    return todos

# PUBLIC_INTERFACE
@app.post("/todos", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED, tags=["Todos"], summary="Create a new todo")
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """Add a new todo item."""
    db_todo = models.Todo(title=todo.title, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# PUBLIC_INTERFACE
@app.patch("/todos/{todo_id}", response_model=schemas.TodoOut, tags=["Todos"], summary="Update a todo")
def update_todo(todo_id: int, update_data: schemas.TodoUpdate, db: Session = Depends(get_db)):
    """Update a todo's title or completion status."""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    update = update_data.dict(exclude_unset=True)
    for key, value in update.items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo

# PUBLIC_INTERFACE
@app.delete("/todos/{todo_id}", response_model=dict, tags=["Todos"], summary="Delete a todo")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo by ID."""
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"deleted": True}
