from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

#RunApp: uvicorn sql_app.main:app --reload

#This sentence is removeable, the purpose is to create a SQLite from scratch
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, name=user.name)

    if db_user:
        raise HTTPException(status_code=400, detail="Name already registered.")

    print(schemas.User)
    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)

    return users


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@app.post('/users/{user_id}/home-works/', response_model=schemas.HomeWork)
def create_home_work_for_user(user_id: int, home_work: schemas.HomeWorkCreate, db: Session = Depends(get_db)) -> models.HomeWork:
    print(schemas.HomeWork)
    return crud.create_user_home_work(db=db, home_work=home_work, user_id=user_id)


@app.get('/home-works/', response_model=List[schemas.HomeWork])
def read_home_works(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    home_works = crud.get_home_works(db, skip=skip, limit=limit)

    return home_works

""" @app.post('/product_class/', response_model=schemas.ProductCategory)
def new_product_category(product_class:schemas.ProductCategoryCreate, db: Session = Depends(get_db)):
    print(schemas.ProductCategoryCreate)
    return crud.create_product_category(input_items = product_class, db = db) """

@app.post('/products/', response_model=schemas.ProductsCreate)
def new_product(product:schemas.ProductsCreate, db: Session = Depends(get_db)):
    print(product)
    return crud.add_product(products = product, db=db)

@app.get("/items/{item_id}")
def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.post('/items/')
def creat_item(item:schemas.Item):
    item_dic = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dic.update({'price with tax' : price_with_tax}) 
    print(item.tax)
    
    return(item_dic)

@app.post('/items/{item_id}/')
def add_itemID(item_id: int , items: schemas.Item):
    return {'item_id':item_id, **items.model_dump()}

