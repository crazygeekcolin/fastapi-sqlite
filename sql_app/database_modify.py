from database import SessionLocal, engine
from sqlalchemy import text, select
import models, schemas
#from models import *
import pandas as pd
import json

connection = engine.connect()

table_name = 'productsCost'
#query = text(f'ALTER TABLE {table_name} DROP 产品名称;')
#connection.execute(query)

db= SessionLocal()
result = db.query(models.Shipping).offset(0).limit(100).all()
print(result)

df = pd.read_excel('../产品编号.xlsx', index_col=0)
#df.rename(columns={'老编码(Steroids)':"老编码"})

print(df.loc[2].to_json(force_ascii=False))
a= df.loc[3].to_json(force_ascii=False)
b=json.loads(a)

print(models.Products(**b))
c= models.Products(**b)
print(type(b))
""" db.add(c)
db.commit()
db.refresh(c) """


#db_product = models.Products()

#results = db.query(models.Products).filter_by(产品名称 = 'bpc157').limit(3).all()
#results: schemas.List[models.Products] = db.query(models.Products).filter(models.Products.产品名称 == 'bpc157').limit(3).all()
#results = db.query(models.Products).limit(3).all()

#results = db.query(models.Products).all()
results = db.execute(select(models.Products)).all()


for i in results[11:13]:
    print(i.Products)
    print(i.Products.产品编号_母表)

print(len(results))

""" for i in results:
    print(i.__dict__, type(i.__dict__))
    i.__dict__.pop('_sa_instance_state')
    #i.__dict__.pop('hashed_password')
    json_string = json.dumps(i.__dict__)
    i_js = json.loads(json_string)
    print(i_js) """
    


