from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class TodoCreate(BaseModel):
    """Pydantic model for creating a new todo."""
    title: str = Field(..., description="Title of the todo")
    completed: bool = Field(default=False, description="Completion status")

# PUBLIC_INTERFACE
class TodoUpdate(BaseModel):
    """Pydantic model for updating a todo."""
    title: str = Field(None, description="Updated title")
    completed: bool = Field(None, description="Updated completion status")

# PUBLIC_INTERFACE
class TodoOut(BaseModel):
    """Pydantic model for outputting a todo."""
    id: int
    title: str
    completed: bool

    class Config:
        orm_mode = True
