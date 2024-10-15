from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
from typing import Optional, Union, List, Any
import pymysql
import os
from connection import get_db_connection

def ai_movie_log_select():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ai_movie.ai_movie_log")
    result = cursor.fetchall()
    connection.close()

    result = [(str(row[0]), row[1]) for row in result]
    return JSONResponse(content={"message": "Database connection successful", "result": result})
