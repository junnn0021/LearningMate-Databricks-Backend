from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from datetime import date
from typing import Optional, Union, List, Any
import pymysql
import os
from app.db_connection import get_db_connection
from app.models import AiMovieResponseReview

def ai_movie_response_review_select():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ai_movie.ai_movie_response_review")
    result = cursor.fetchall()
    connection.close()

    result = [(str(row[0]), row[1]) for row in result]
    return JSONResponse(content={"message": "Database connection successful", "result": result})

#call junseok code
def ai_movie_review_call_procedure(review_data: AiMovieResponseReview):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            result_id = cursor.var(bigint)  
            cursor.callproc(
                'usp_ai_review_I',
                (
                    review_data.ai_response_id,
                    review_data.ai_user_review,
                    review_data.ai_user_score,
                    result_id,
                )
            )
            connection.commit()
            return JSONResponse(content={"message": "Review registered successfully", "result_id": result_id.getvalue()}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()
