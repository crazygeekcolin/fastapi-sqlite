from typing import List, Tuple, Sequence, Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session


from . import crud, models, schemas, helper
from .database import SessionLocal, engine

from pydantic import BaseModel

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

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


""" def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict) """

def get_user_new(username:str, db:Session = SessionLocal()):
       user_list = []
       for i in crud.get_users(db =db):
           user_list.append(i.name)
           if username in user_list:
               #user: models.User | None = db.query(models.User).filter(models.User.name ==username).first()
               user = crud.get_user_by_name(db=db, name= username)
                #Make a copy so when query next time, the Python is working. If not will raise Error!
               user_dict= user.__dict__.copy()
               return user_dict


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user_new(username = token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)],
):
    if current_user['is_active'] is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = get_user_new(username=form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    #Create a temporary User
    user = models.User(name = user_dict['name'],hashed_password = user_dict['hashed_password'])
    if not helper.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.name, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)],
):
    return current_user


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)

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
    print(home_works)
    return home_works

@app.post('/products/', response_model=schemas.Product, tags= ['Product'])
def new_product(productCategory: schemas.ProductCategory ,product:schemas.ProductsCreate, db: Session = Depends(get_db)):
    print(product)
    return crud.add_product(products = product, productCategory = productCategory ,db=db)

@app.post('/products_cost/', response_model= schemas.ProductCost, tags= ['Product'])
def new_product_cost(product_cost: schemas.ProductCostCreate , db: Session =Depends(get_db)):
    print(product_cost)
    return crud.add_product_cost(productsCost=product_cost, db=db)

@app.post('/customer/', response_model= schemas.Customer)
def new_customer(customer: schemas.CustomerCreate, db:Session = Depends(get_db)):
    print(customer)
    return crud.add_customer(customer=customer, db=db)

@app.post('/payment/', response_model=schemas.Payment)
def new_payment(currency: schemas.Currency, payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    print(payment)
    print(currency)
    return crud.add_payment(currency= currency, payment= payment, db=db)

@app.post('/shipping/', response_model=schemas.Shipping)
def new_shipping(method:schemas.Method, currency: schemas.Currency, shipping: schemas.ShippingCreate, db: Session = Depends(get_db)):
    print(method, currency,shipping)
    return crud.add_shipping(method=method, currency=currency, shipping= shipping, db=db)

@app.post('/order/',response_model= schemas.Order)
def new_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.add_order(order=order, db=db)


""" @app.get("/items/{item_id}")
def read_item(item_id: str, q: str | None = None, short: bool = False):
    item: dict[str, str] = {"item_id": item_id}
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
    return {'item_id':item_id, **items.model_dump()} """
    

#Get products by name
@app.get('/products/name/{query}', response_model= List[Tuple[schemas.ProductQuery]], tags=['Product'])
def query_product(query: str, db:Session = Depends(get_db)):
    products = crud.query_product(db, text = query)
    return products

#Get all products
@app.get('/products/', response_model=List[schemas.ProductQuery], tags=['Product'])
def query_product1(skip:int =0, limit: int =100, db: Session = Depends(get_db)):
    result = crud.query_product1(skip=skip, limit=limit ,db=db)
    return result

#Get products by 产品编号
@app.get('/products/code/{query}', response_model= List[schemas.ProductQuery], tags=['Product'])
def query_product_code(text:str, db:Session = Depends(get_db)):
    return crud.query_product_code(text= text, db=db)

#Get products cost
@app.get('/products_cost/', response_model= List[schemas.ProductCostQuery], tags= ['Product'])
def query_products_cost(skip:int =0, limit: int =100, db: Session = Depends(get_db)):
    return crud.query_products_cost(skip=skip, limit=limit, db=db)

#Get products cost by name
@app.get('/product_cost/name/{text}', response_model=List[schemas.ProductCostQuery], tags=['Product'])
def query_products_cost_by_name(text: str, skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):# -> List[Row[Tuple[str, str, str, Any, Any, datetime]]]:
    return crud.query_products_cost_by_name(db = db, skip=skip, limit= limit, text = text)

#Get latest payments
@app.get('/payment/', response_model=List[schemas.Payment], tags= ['Payment'])
def query_payments(skip: int = 0, limit: int = 100, db:Session = Depends(get_db)):
    return crud.query_payments(skip= skip, limit= limit, db=db)

#Get latest payments by customer
@app.get('/payment/customer/{text}', response_model=List[schemas.Payment], tags=['Payment'])
def query_payments_customer(text:str, skip:int = 0, limit:int =100, db:Session =Depends(get_db)):
    return crud.query_payments_customer(db = db, text= text, skip= skip, limit= limit)

#Get latest payments by sales name
@app.get('/payment/sales/{text}', response_model=List[schemas.Payment], tags=['Payment'])
def query_payments_sales(text:str, skip:int = 0, limit:int =100, db:Session =Depends(get_db)):
    return crud.query_payments_sales(db = db, text= text, skip= skip, limit= limit)

#Get customer by name
@app.get('/customer/name/{text}', response_model=List[schemas.Customer], tags=['Customer'])
def query_customer_names(text:str, db:Session =Depends(get_db)):
    return crud.query_customer_name(db = db, text= text)