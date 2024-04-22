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
    # id: None
    # path: None
    # author: None
    public: Union[bool, None] = None
    # created_at: None
    likes: Union[int, None] = None


class FavouritesCreate(BaseModel):
    id: int
    id_file: int
    user_id: int
