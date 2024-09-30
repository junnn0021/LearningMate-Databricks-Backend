from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
from typing import Optional, Union, List, Any
from fastapi import FastAPI
from pydantic import BaseModel, Field
import pymysql
import os

app = FastAPI()

class NewTable(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    hire: date
    job_title: str

    class Config:
        orm_mode = True

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
    return {"Hello": "Junseok World"}

@app.get("/new_table")
def read_new_table():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM new_table")
        result = cursor.fetchall()
        connection.close()
        return JSONResponse(content={"message": "New Table data", "result": result})
    except Exception as e:
        return JSONResponse(content={"message": "Error occurred", "error": str(e)}, status_code=500)

@app.post("/new_table")
async def create_new_table(new_table: NewTable):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO new_table (first_name, last_name, email, hire, job_title) VALUES (%s, %s, %s, %s, %s)", 
                      (new_table.first_name, new_table.last_name, new_table.email, new_table.hire, new_table.job_title))
        connection.commit()
        connection.close()
        return JSONResponse(content={"message": "New table created successfully"}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"message": "Error occurred", "error": str(e)}, status_code=500)

@app.get("/new_table/{new_table_id}")
def read_new_table(new_table_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM new_table WHERE id = %s", (new_table_id,))
        result = cursor.fetchone()
        connection.close()
        if result:
            return JSONResponse(content={"message": "New table found", "result": result})
        else:
            return JSONResponse(content={"message": "New table not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": "Error occurred", "error": str(e)}, status_code=500)

@app.put("/new_table/{new_table_id}")
async def update_new_table(new_table_id: int, new_table: NewTable):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE new_table SET first_name = %s, last_name = %s, email = %s, hire = %s, job_title = %s WHERE id = %s", 
                      (new_table.first_name, new_table.last_name, new_table.email, new_table.hire, new_table.job_title, new_table_id))
        connection.commit()
        connection.close()
        return JSONResponse(content={"message": "New table updated successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error occurred", "error": str(e)}, status_code=500)

@app.delete("/new_table/{new_table_id}")
async def delete_new_table(new_table_id: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM new_table WHERE id = %s", (new_table_id,))
        connection.commit()
        connection.close()
        return JSONResponse(content={"message": "New table deleted successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Error occurred", "error": str(e)}, status_code=500)