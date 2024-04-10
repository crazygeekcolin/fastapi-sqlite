from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone, date
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

class ProductCostCreate(BaseModel):
    产品编号: str
    产品规格: str = Field(title='产品规格', description='格式小写不加vials 5mg')
    成本: float = Field(title='产品成本', description='格式：数字')
    #update: datetime = Field(default_factory = datetime_now)
    
class ProductCost(ProductCostCreate):
    id: int
    update: datetime

class ProductCategory(str, Enum):
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
    产品类别: ProductCategory| None = None

class ProductQuery(Product):
    产品成本记录: List[ProductCost] = []
    
    

class CustomerCreate(BaseModel):
    业务员: str
    客户名: str
    联系方式: str|None
    网站: str|None
    
class Customer(CustomerCreate):
    id: int

class Currency(str, Enum):
    CNY = 'CNY 人民币'
    USD = 'USD 美元'
    HKD = 'HKD 港币'
    EUR = 'EUR 欧元'
    GBP = 'GBP 英镑'
     
    
class PaymentCreate(BaseModel):
    日期: date = Field(title= '日期')
    金额: int
    #币种 = enum
    业务员: str
    customer: str
    是否预付款: bool| None = Field(default= 0)
    备注: None|str = Field(default =None)
    
class Payment(PaymentCreate):
    id: int
    币种: Currency
    

class Method(str, Enum):
    美仓李帅直发 = '美仓李帅直发'
    中国直发英国 = '中国直发英国'
    中国直发德国= '中国直发德国'
    中国直发UPS= '中国直发UPS'
    

class ShippingCreate(BaseModel):
    日期: date = Field(default_factory=date_now)
    业务员: str
    收款说明: str
    收款金额: str
    #币种: str
    #途径
    单号: str
    转单号: str
    状态: str
    收件人: str
    国家:str
    地址: str
    电话: str
    customer: str
    明细备注: str
    
class Shipping(ShippingCreate):
    id: int
    币种: str
    途径: Method

class OrderCreate(BaseModel):
    发货单ID: int
    产品编号: str
    产品规格: str
    产品数量: int
    产品颜色: str
    是否装盒: bool|None = Field(default= 1)
    备注: str

class Order(OrderCreate):
    id: int

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