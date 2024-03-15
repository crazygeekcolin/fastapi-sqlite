from typing import List, Optional
from pydantic import BaseModel


class HomeWorkBase(BaseModel):
    title: str
    description: Optional[str] = "-"

class HomeWorkCreate(HomeWorkBase):
    pass


class HomeWork(HomeWorkBase):
    #model_config = ConfigDict(from_attributes=True)
    #https://docs.pydantic.dev/latest/concepts/models/
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    #model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    home_works: List[HomeWork] = []

    class Config:
        orm_mode = True

