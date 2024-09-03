from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
from typing import Optional, Union, List, Any
from fastapi import FastAPI
from pydantic import BaseModel, Field
import pymysql
import os
 
app = FastAPI()

class Item(BaseModel):
     name: str
     phone : Optional[int] = None # phone의 값을 Optional로 지정, 기본값을 None으로 설정
     description : Union[int,float] # int, float 중 무엇이 들어오건 상관 없음
     address : str = Field(example='서울특별시 ㅇㅇ구') #str 타입이고, 예시 설명을 추가
     status : List[Any] = Field([], description = '텍스트로 상태를 설명해주세요') # 어떤 타입이든 받을 수 있는 리스트인데 기본 값은 비어있는 list[]
 
@app.post("/items/")
async def create_item(item: Item):
     return item


@app.get("/")
def read_root():
    return {"Hello": "Junseok World"}


mysql_host = os.environ['MYSQL_HOST']
mysql_user = os.environ['MYSQL_USER']
mysql_password = os.environ['MYSQL_PASSWORD']
mysql_database = os.environ['MYSQL_DATABASE']

def get_db_connection():
    connection = pymysql.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    return connection

@app.get("/test-db")
def test_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM new_table")
    result = cursor.fetchall()
    connection.close()

    result = [(str(row[0]), row[1]) for row in result]

    return JSONResponse(content={"message": "Database connection successful", "result": result})
