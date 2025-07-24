from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(..., max_length=200)
    body: str = Field(..., max_length=2000)
    tags: Optional[List[str]] = []


class Post(PostBase):
    id: UUID
    createdDate: datetime
    updatedDate: datetime


class Response(BaseModel):
    statusCode: int
    body: str = ""
    headers: dict = {
        "Content-Type": "application/json"
    }
