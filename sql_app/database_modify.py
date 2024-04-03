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

for i in result:
    print(i.__dict__)

print('ok')

df = pd.read_excel('../产品编号.xlsx', index_col=0)
#df.rename(columns={'老编码(Steroids)':"老编码"})

print(df.loc[2].to_json(force_ascii=False))
a= df.loc[3].to_json(force_ascii=False)
b=json.loads(a)


results = db.query(models.Products).all()

for i in results[:2]:
    print(i.__dict__, type(i.__dict__))
    ijson= i.__dict__.pop('_sa_instance_state')
    print(i.__dict__)
    json_string = json.dumps(i.__dict__)
    i_js = json.loads(json_string)
    print(i_js)
    


""" for i in range(len(df)):
    if i.产品编号  """

print(models.Products(**b))
c= models.Products(**b)
print(type(b))
""" db.add(c)
db.commit()
db.refresh(c) """


#db_product = models.Products()

