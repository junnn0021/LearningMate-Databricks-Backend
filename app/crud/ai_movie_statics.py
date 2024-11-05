from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
from typing import Optional, Union, List, Any
import pymysql
import os
from app.db_connection import get_db_connection

# def ai_movie_response_select():
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM ai_movie.ai_movie_statics")
#     result = cursor.fetchall()
#     connection.close()

#     result = [(str(row[0]), row[1]) for row in result]
#     return JSONResponse(content={"message": "Database connection successful", "result": result})

def get_movie_statics_movie_actor_call_procedure():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_statics_movie_actor_L'
            )
            result = cursor.fetchall()
        connection.commit()
        return JSONResponse(result, content={"message": "Request was successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()
        
def get_movie_statics_movie_count_call_procedure():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_statics_movie_count_L'
            )
            result = cursor.fetchall()
        connection.commit()
        return JSONResponse(result, content={"message": "Request was successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()
        
def get_movie_statics_movie_genre_call_procedure():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_statics_movie_genre_L'
            )
            result = cursor.fetchall()
        connection.commit()
        return JSONResponse(result, content={"message": "Request was successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()
        
def get_movie_statics_movie_title_call_procedure():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_statics_movie_title_L'
            )
            result = cursor.fetchall()
        connection.commit()
        return JSONResponse(result, content={"message": "Request was successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()
        
def get_movie_statics_request_count_call_procedure():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_statics_request_count_L'
            )
            result = cursor.fetchall()
        connection.commit()
        return JSONResponse(result, content={"message": "Request was successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()
        
def get_movie_statics_user_score_call_procedure():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_statics_user_score_L'
            )
            result = cursor.fetchall()
        connection.commit()
        return JSONResponse(result, content={"message": "Request was successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()