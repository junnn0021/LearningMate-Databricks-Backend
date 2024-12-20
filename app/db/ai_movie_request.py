from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
from typing import Optional, Union, List, Any
import pymysql
import os
from app.db_connection import get_db_connection
from app.models import AiMovieRequest
def ai_movie_request_select():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ai_movie.ai_movie_request")
    result = cursor.fetchall()
    connection.close()
    result = [(str(row[0]), row[1]) for row in result]
    return JSONResponse(content={"message": "Database connection successful", "result": result})

def ai_movie_request_call_procedure3(request_data: AiMovieRequest):
    print("request_data : {0}".format(request_data))
    print("ai_request_text : {0}".format(request_data["ai_request_text"]))
    print("ai_request_id : {0}".format(request_data["ai_request_id"]))
    print("request_ip : {0}".format(request_data["request_ip"]))
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_request_I',
                (request_data["ai_request_text"], "", request_data["request_ip"])
            )
            result = cursor.fetchall()
            print("result : {0}".format(result))
        connection.commit()
        return JSONResponse(content={"message": "Request saved successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()

def save_ai_movie_request_call_procedure(request_data: AiMovieRequest):
    print("save_ai_movie_request_call_procedure request_data : {0}".format(request_data))
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_request_I', 
                (request_data.ai_request_text, request_data.request_ip, 0)
            )
            # OUT 매개변수 읽기
            cursor.execute("SELECT @result_id := LAST_INSERT_ID();")
            result_id = cursor.fetchone()[0]

            print("save_ai_movie_request_call_procedure 성공 결과: {0}".format(result_id))
        connection.commit()
        return JSONResponse(content={"result_id": result_id, "message": "Request saved successfully"}, status_code=200)
    except Exception as e:
        print("save_ai_movie_request_call_procedure 예외처리 : {0}".format(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()