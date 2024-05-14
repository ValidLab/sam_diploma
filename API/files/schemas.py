from typing import Union
from datetime import datetime
from pydantic import BaseModel


class FileCreate(BaseModel):
    path: str
    author: str
    public: bool
    created_at: datetime
    likes: int


class FileUpdate(BaseModel):
    public: Union[bool, None] = None
    likes: Union[int, None] = None


class FavouritesCreate(BaseModel):
    id_file: int
    user_id: int
