from sqlalchemy.orm import Session
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

def add_product(db: Session, products = schemas.ProductsCreate, productCategory = schemas.ProducCategory):
    
    db_product = models.Products(**products.model_dump(), 产品类别 = productCategory)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

def add_product_cost(db: Session, productsCost = schemas.ProductCostCreate):
    db_product_cost = models.ProductsCost(**productsCost.model_dump())
    db.add(db_product_cost)
    db.commit()
    db.refresh(db_product_cost)
    
    return db_product_cost

def add_customer(db: Session, customer = schemas.CustomerCreate):
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    return db_customer
    