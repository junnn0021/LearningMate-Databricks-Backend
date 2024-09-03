from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
import pymysql
import os
 
app = FastAPI()
 
 
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
