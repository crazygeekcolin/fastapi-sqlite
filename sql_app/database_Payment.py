from database import SessionLocal, engine
#from sqlalchemy import text, select
import models, schemas
#from models import *
import pandas as pd
import json
from datetime import datetime, date

db= SessionLocal()
df = pd.read_excel('../业务收款.xlsx', index_col=0)
df['customer'] = df['Customer']
df.drop(columns='Customer', inplace=True)
df['是否预付款']=df['预付款/补款']
df.drop(columns='预付款/补款', inplace=True)

#Covert the unix date to date
#df['日期'] = df['日期'].dt.strftime('%Y-%m-%d')
print(df['日期'].iloc[2])
print(df['币种'].unique())
df['币种'].replace({'USD Zelle':'USD 美元', 'CNY人民币':'CNY 人民币', 'USD': 'USD 美元', 'HKD港币': 'HKD 港币'}, inplace=True)
print(df['币种'].unique())

#Convert it to js
def add_db(row, primary_key_check = None):
    #Get the json format, need to convert later to sqlalchemy models
    json_string= row.to_json(date_format = 'iso',force_ascii=False)
    js = json.loads(json_string)
    #print(js, 'add_db')
    return js

#Add payment
for i in range(len(df)):
    row = add_db(df.iloc[i])
    row['日期'] = datetime.fromisoformat(row['日期'])
    
    #print(type(row['日期']), row)
    if row:
        db_product_cost= models.Payment(**row)
        db.add(db_product_cost)
        db.commit()
        db.refresh(db_product_cost)


#Add customer
df = pd.read_excel('../客户资料.xlsx', index_col=0)

result= db.query(models.Customer.客户名).all()
result_list = []
for i in result:
    result_list.extend(i)
#print(result_list)

for i in range(len(df)):
    row = add_db(df.iloc[i])
    if row['客户名'] not in result_list:
        db_product_cost= models.Customer(**row)
        db.add(db_product_cost)
        db.commit()
        db.refresh(db_product_cost)
