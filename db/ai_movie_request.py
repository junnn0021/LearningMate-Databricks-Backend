from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
from typing import Optional, Union, List, Any
import pymysql
import os
from connection import get_db_connection

def ai_movie_request_select():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ai_movie.ai_movie_request")
    result = cursor.fetchall()
    connection.close()

    result = [(str(row[0]), row[1]) for row in result]
    return JSONResponse(content={"message": "Database connection successful", "result": result})

#call test.1
def ai_movie_request_call_procedure(ai_request_text:str, date:str, request_ip:int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("call ai_movie.usp_ai_request_I("+ai_request_text+","+date+","+str(request_ip)+")")
    result = cursor.fetchall()
    connection.close()

    result = [(str(row[0]), row[1]) for row in result]
    return JSONResponse(content={"message": "Database connection successful", "result": result})

#call test.2
async def ai_movie_request_call_procedure2(ai_request_text:str, request_ip:int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc('ai_movie.usp_ai_request_I', [ai_request_text, request_ip])
            result = await cursor.fetchall()
        connection.commit()
        return JSONResponse(content={"message": "Item updated successfully"}, status_code=200)
    except Exception as e:
        return {"error": str(e)}
    finally:
        connection.close()