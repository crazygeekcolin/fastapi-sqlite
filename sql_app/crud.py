from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas
from .helper import *


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_hashed_password(plain_text_password=user.password)
    db_user = models.User(name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_home_works(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.HomeWork).offset(skip).limit(limit).all()


def create_user_home_work(db: Session, home_work: schemas.HomeWorkCreate, user_id: int) :
    db_home_work = models.HomeWork(**home_work.model_dump(), owner_id=user_id)
    print(home_work)
    db.add(db_home_work)
    db.commit()
    db.refresh(db_home_work)

    return db_home_work

""" def create_product_category(db:Session, input_items:schemas.ProductCategoryCreate) :

    db_product_category = models.Products_class(产品类别1 = input_items.产品类别1)
    print(db_product_category)
    db.add(db_product_category)
    db.commit()
    db.refresh(db_product_category)
    
    return db_product_category """

def add_product(db: Session, products: schemas.ProductsCreate, productCategory: schemas.ProductCategory):
    
    db_product = models.Products(**products.model_dump(), 产品类别 = productCategory)
    print(db_product)
    print(products.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

def add_product_cost(db: Session, productsCost: schemas.ProductCostCreate):
    db_product_cost = models.ProductsCost(**productsCost.model_dump())
    db.add(db_product_cost)
    db.commit()
    db.refresh(db_product_cost)
    
    return db_product_cost

def add_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    return db_customer

def add_payment(db: Session, currency: schemas.Currency, payment: schemas.PaymentCreate):
    db_payment = models.Payment(币种 = currency, **payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    return db_payment

def add_shipping(db:Session, method:schemas.Method, currency: schemas.Currency, shipping: schemas.ShippingCreate):
    db_shipping = models.Shipping(途径 = method, 币种 = currency, **shipping.model_dump())
    db.add(db_shipping)
    db.commit()
    db.refresh(db_shipping)
    
    return db_shipping

def add_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order


def query_product(db: Session, text: str):
    """ stmt = select(models.Products.产品编号
              , models.Products.产品名称
              , models.Products.产品类别
              , #Products.产品成本记录).join(ProductsCost).filter(Products.产品名称 == 'Sermorelin\xa0(GRF1-29)')
              models.Products.产品成本记录).join(models.ProductsCost)
     """
    stmt = select(models.Products).filter(models.Products.产品名称.like(f'%{text}%'))
    return db.execute(stmt).all()

def query_product1(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Products).offset(skip).limit(limit).all()

