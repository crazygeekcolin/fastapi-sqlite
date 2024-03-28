from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from enum import Enum

def date_now() -> datetime:
    return datetime.now(timezone.utc).date()

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

    产品名称: str|None = Field(title = "填写产品名称", description=  '描述', default= None)
    产品编号: str|None = Field(title='产品编号', description='Example:G008 可以空着', default= None)
    老编码: str|None = Field(title='老编号', description='粉末之前老编码 TE,TC 可以空着', default= None)
    
class Product(ProductsCreate):
    id: int
    产品类别: ProducCategory| None = None
    
    
class ProductCostCreate(BaseModel):
    产品编号: str
    产品规格: str = Field(title='产品规格', description='格式小写不加vials 5mg')
    成本: float = Field(title='产品成本', description='格式：数字')
    #update: datetime = Field(default_factory = datetime_now)
    
class ProductCost(ProductCostCreate):
    id: int
    update: datetime

class CustomerCreate(BaseModel):
    业务员: str
    客户名: str
    联系方式: str
    网站: str
    
class Customer(CustomerCreate):
    id: int

class Currency(str, Enum):

class PaymentCreate(BaseModel):
    日期
    金额
    #币种 = enum
    业务员
    customer
    备注
    

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