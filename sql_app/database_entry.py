from database import SessionLocal, engine
from sqlalchemy import text, select
import models, schemas
#from models import *
import pandas as pd
import json

db= SessionLocal()
#results = db.query(models.Products.产品名称, models.Products.产品编号).all()
results = db.query(models.Products.产品编号).all()

#Create a list with Primary KEY 
result_list =[]
for i in results:
    result_list.append(i[0])
print(result_list)

df = pd.read_excel('../产品编号.xlsx', index_col=0)
##Data operation
def strip_series(series):
    ###Loop over items of pandas series and move their blank space in head and tail
    for i in range(len(series)):
        if type(series.iloc[i]) == str:
            series.iloc[i] = series.iloc[i].strip()

for i in range(len(df)):
    strip_series(df.iloc[i])

print(df.loc[2])

print(df.iloc[2].to_json(force_ascii=False))

def add_db(row, primary_key_check: str):
    #Get the json format, need to convert later to sqlalchemy models
    json_string= row.to_json(force_ascii=False)
    js = json.loads(json_string)
    print(js, 'add_db')
    
    if js[primary_key_check] not in result_list:
        return js



for i in range(len(df)):
    row = add_db(df.iloc[i], primary_key_check= '产品编号')
    if row:
        db_product= models.Products(**row)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        

print(add_db(df.iloc[4], primary_key_check='产品编号'))
""" for i in range(len(df)):
    
    if df.iloc[i]['产品编号'] not in result_list:
        
        db.add(df.iloc[i])
        db.commit()
        db.refresh(df.iloc[i]) """


