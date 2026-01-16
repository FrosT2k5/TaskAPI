from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, UTC

def current_time() -> datetime:
    return datetime.now(UTC)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="pending", max_length=20)
    created_at: datetime = Field(default_factory=current_time)
    updated_at: datetime = Field(default_factory=current_time)
