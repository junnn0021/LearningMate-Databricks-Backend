from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
from typing import Optional, Union, List, Any
from fastapi import FastAPI
import pymysql
import os

app = FastAPI()

def get_db_connection():
    connection = pymysql.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database=os.environ['MYSQL_DATABASE']
    )
    return connection

@app.get("/")
def read_root():
    return {"Hello": "Junseok World."}

@app.get("/test-db")
def test_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM new_table")
    result = cursor.fetchall()
    connection.close()

    result = [(str(row[0]), row[1]) for row in result]

    return JSONResponse(content={"message": "Database connection successful", "result": result})
    
@app.post("/items")
async def create_item(id: int, first_name: str, last_name: str, email: str, hire: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO new_table (id, first_name, last_name, email, hire) VALUES (%s, %s, %s, %s, %s)", (id, first_name, last_name, email, hire))
    connection.commit()
    connection.close()
    return JSONResponse(content={"message": "Item created successfully"}, status_code=201)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM new_table WHERE id = %s", (item_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        result = (str(result[0]), result[1])
        return JSONResponse(content={"message": "Item found", "result": result})
    else:
        return JSONResponse(content={"message": "Item not found"}, status_code=404)

@app.put("/items/{item_id}")
async def update_item(item_id: int, first_name: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE new_table SET first_name = %s WHERE id = %s", (first_name, item_id))
    connection.commit()
    connection.close()
    return JSONResponse(content={"message": "Item updated successfully"}, status_code=200)

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM new_table WHERE id = %s", (item_id,))
    connection.commit()
    connection.close()
    return JSONResponse(content={"message": "Item deleted successfully"}, status_code=200)