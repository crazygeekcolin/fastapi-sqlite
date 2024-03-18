from database import SessionLocal, engine
from sqlalchemy import text

connection = engine.connect()

table_name = 'productsCost'
#query = text(f'ALTER TABLE {table_name} DROP 产品名称;')

connection.execute(query)