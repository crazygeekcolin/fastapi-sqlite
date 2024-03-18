from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User1(Base):
    __tablename__ = 'users1'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    home_works = relationship('HomeWork', back_populates='owner')


class HomeWork(Base):
    __tablename__ = 'home_works'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users1.id'))

    owner = relationship('User1', back_populates='home_works')
    
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    产品名称 = Column(String)
    产品编号 = Column(String, index=True, unique=True)
    老编码 = Column(String)
    产品类别 = Column(String, ForeignKey('products_class.产品类别1'))
    
    产品类别_子表 = relationship('Products_class', back_populates= '产品类别_母表')
    
    产品编号_母表 = relationship('productsCost', back_populates='产品编号_子表')

class Products_class(Base):
        __tablename__ = 'products_class'
        id = Column(Integer, primary_key=True, index=True)
        产品类别1 = Column(String, index=True)
        产品类别_母表 = relationship('Products', back_populates= '产品类别_子表')

class ProductsCost(Base):
    __tablename__ = 'productsCost'
    id = Column(Integer, primary_key=True, index=True)
    产品名称 = Column(String)
    产品编号 = Column(String, ForeignKey('products.产品编号'))
    产品规格 = Column(String)
    成本 = Column(Integer)
    update = Column(DateTime, server_default=func.now())
    产品编号_子表 = relationship('products', back_populates='产品编号_母表')

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    salesperson_parent = relationship('Customer', back_populates='salesperson_child')
    业务员_order_parent:
    业务员_payment_parent:

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    salesperson = Column(String, ForeignKey('User.name'))
    客户名 = Column(String, unique=True, index=True)
    联系方式 = Column(String)
    网站 = Column(String)

    salesperson_child = relationship('User', back_populates= 'salesperson_parent')
    payments_parent = relationship('Currency', back_populates='owner')
    shipping_parent: 
    customer_parent:

class Currency(Base):
    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, unique=True, index=True)
    
    payments_parent = relationship()

