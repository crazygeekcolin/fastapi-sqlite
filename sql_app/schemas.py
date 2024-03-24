from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum


class HomeWorkBase(BaseModel):
    title: str
    description: Optional[str] = "-"

class HomeWorkCreate(HomeWorkBase):
    pass


class HomeWork(HomeWorkBase):
    model_config = ConfigDict(from_attributes=True)
    #https://docs.pydantic.dev/latest/concepts/models/
    id: int
    owner_id: int

    """  class Config:
        orm_mode = True """


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    home_works: List[HomeWork] = []

    """  class Config:
        orm_mode = True """
        
        
""" class ProductCategoryCreate(BaseModel):
    产品类别1: str | None = None
    #productCategory: str | None = None

class ProductCategory(ProductCategoryCreate):
    model_config = ConfigDict(from_attributes= True)
    id: int """

class ProducCategory(str, Enum):
    peptide = 'Peptide'
    steroid = 'Steroids'
    sarm = 'Sarm'
    other = 'Others'

class ProductsCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    产品名称: str|None = Field(title = "填写产品名称", description=  '描述', default= None)
    产品编号: str|None = Field(title='产品编号', description='Example:G008 可以空着', default= None)
    老编码: str|None = Field(title='产品编号', description='粉末之前老编码 TE,TC 可以空着', default= None)
    产品类别: ProducCategory| None = None
    

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "price": 35.4,
                    "tax": 3.2,
                    "description": "A very nice Item",
                    "name": "Foo"
                }
            ]
        }
    }