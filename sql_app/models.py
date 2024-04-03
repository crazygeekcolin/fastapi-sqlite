from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
#from .database import Base #Used in FastAPI

from database import Base #Used in normal python


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
    #产品类别 = Column(String, ForeignKey('products_class.产品类别1'))
    产品类别 = Column(String)
    
    #产品类别_子表 = relationship('Products_class', back_populates= '产品类别_母表')
    
    产品编号_母表 = relationship('ProductsCost', back_populates='产品编号_子表')
    产品编号_parent = relationship('Order', back_populates ='产品编号_child')

""" class Products_class(Base):
        __tablename__ = 'products_class'
        
        id = Column(Integer, primary_key=True, index=True)
        产品类别1 = Column(String, index=True)
        产品类别_母表 = relationship('Products', back_populates= '产品类别_子表') """

class ProductsCost(Base):
    __tablename__ = 'productsCost'
    
    id = Column(Integer, primary_key=True, index=True)
    #产品名称 = Column(String)
    产品编号 = Column(String, ForeignKey('products.产品编号'))
    产品规格 = Column(String)
    成本 = Column(Numeric)
    update = Column(DateTime, server_default=func.now())
    #update = Column(DateTime)
    产品编号_子表 = relationship('Products', back_populates='产品编号_母表')

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    #业务员_customer_parent = relationship('Customer', back_populates = '业务员_customer_child')
    salesperson_parent = relationship('Customer', back_populates='salesperson_child')
   # 业务员_order_parent:relationship('Curr')
    业务员_payment_parent = relationship('Payment', back_populates= '业务员_payment_child')
    业务员_shipping_parent = relationship('Shipping', back_populates= '业务员_shipping_child')

    
class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True, index=True)
    业务员 = Column(String, ForeignKey('users.name'))
    客户名 = Column(String, unique=True, index=True)
    联系方式 = Column(String)
    网站 = Column(String)

    salesperson_child = relationship('User', back_populates= 'salesperson_parent')
    customer_payments_parent = relationship('Payment', back_populates='customer_payments_child')
    #customer_order_parent: 
    customer_shipping_parent = relationship('Shipping', back_populates= 'customer_shipping_child')


class Payment(Base):
    __tablename__ = '业务收款'

    id = Column(Integer, primary_key=True, index=True)
    日期 = Column(Date)
    金额 = Column(Numeric)
    #币种 = Column(String,ForeignKey('currency.currency'))
    币种 = Column(String)
    业务员 = Column(String, ForeignKey('users.name'))
    customer = Column(String, ForeignKey('customers.客户名'))
    是否预付款 = Column(Boolean)
    备注 =Column(String)
    
    customer_payments_child = relationship('Customer', back_populates='customer_payments_parent')
    #币种_子表 = relationship('Currency', back_populates='币种_母表')
    业务员_payment_child = relationship('User', back_populates= '业务员_payment_parent')
    
    
class Shipping(Base):
     __tablename__ = '发货单'
     
     id = Column(Integer, primary_key=True, index=True)
     日期 = Column(Date)
     业务员 = Column(String, ForeignKey('users.name'))
     收款说明 = Column(String)
     收款金额 = Column(String)
     币种 = Column(String)
     途径 = Column(String)
     备注 = Column(String)
     单号 = Column(String)
     转单号 = Column(String)
     状态 = Column(String)
     收件人 = Column(String)
     国家 = Column(String)
     地址 = Column(String)
     电话 = Column(String)
     customer = Column(String, ForeignKey('customers.客户名'))
     明细备注 = Column(String)

     业务员_shipping_child = relationship('User', back_populates= '业务员_shipping_parent')
     customer_shipping_child = relationship('Customer', back_populates= 'customer_shipping_parent')
     发货单ID_parent =  relationship('Order', back_populates='发货单ID_child')


class Order(Base):
    __tablename__ = '订单'
    id = Column(Integer, primary_key=True, index=True)
    发货单ID = Column(Integer, ForeignKey('发货单.id'))
    产品编号 = Column(String, ForeignKey('products.产品编号'))
    产品规格 = Column(String)
    产品数量 = Column(Integer)
    产品颜色 = Column(String)
    是否装盒 = Column(Boolean)
    备注 =Column(String)
    
    产品编号_child = relationship('Products', back_populates ='产品编号_parent')
    发货单ID_child =  relationship('Shipping', back_populates ='发货单ID_parent')
    

""" class Currency(Base):
    __tablename__ = 'currency'
    
    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, unique=True, index=True)
    
    币种_母表 = relationship('Payment', back_populates='币种_子表') """

""" class Customer(Base):
    __tablename__ = '客户'
    
    id = Column(Integer, primary_key=True, index=True)
    业务员 = Column(String, ForeignKey('users.name'))
    联系方式 = Column(String)
    网站 = Column(String)
    
    业务员_customer_child = relationship('User', back_populates = '业务员_customer_parent')
 """
 
