from database import SessionLocal, engine
from sqlalchemy import text, select
import models, schemas
#from models import *
import pandas as pd
import json

db= SessionLocal()
#results = db.query(models.Products.产品名称, models.Products.产品编号).all()
#results = db.query(models.Products.产品编号).all()

#Create a list with Primary KEY 

df = pd.read_excel('../产品成本.xlsx', index_col=0)
##Data operation
def strip_series(series):
    ###Loop over items of pandas series and move their blank space in head and tail
    for i in range(len(series)):
        if type(series.iloc[i]) == str:
            series.iloc[i] = series.iloc[i].strip()

for i in range(len(df)):
    strip_series(df.iloc[i])

result_list = []

print(df.iloc[2].to_json(force_ascii=False))
print(df.产品编号.unique(), len(df.产品编号.unique()))

def add_db(row, primary_key_check = None):
    #Get the json format, need to convert later to sqlalchemy models
    json_string= row.to_json(force_ascii=False)
    js = json.loads(json_string)
    print(js, 'add_db')
    return js
    
    
for i in range(len(df)):
    row = add_db(df.iloc[i])
    if row:
        db_product_cost= models.ProductsCost(**row)
        db.add(db_product_cost)
        db.commit()
        db.refresh(db_product_cost)

add_db(df.iloc[4])
""" for i in range(len(df)):
    
    if df.iloc[i]['产品编号'] not in result_list:
        
        db.add(df.iloc[i])
        db.commit()
        db.refresh(df.iloc[i]) """

