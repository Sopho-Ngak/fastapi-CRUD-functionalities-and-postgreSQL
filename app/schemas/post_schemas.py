from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime
import uuid


class PostBase(BaseModel):
    id: Union[uuid.UUID, None] = None
    title: str
    body: str
    published: Union[bool, None] = None
    created_at: datetime

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = None

    class Config:
        orm_mode = True
