from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from app.db_connection import get_db_connection
from app.models import AiMovieLog

def save_ai_movie_log_call_procedure(log_data: AiMovieLog):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'usp_ai_movie_log_I',
                (
                    log_data.log_type,
                    log_data.log_msg,
                    log_data.log_time,
                    log_data.log_name,
                    log_data.function_name,
                    log_data.line_no,
                    log_data.process_id,
                    log_data.process_name,
                    log_data.thread_id,
                    log_data.thread_name,
                    log_data.work_name,
                    log_data.stack,
                    log_data.path,
                )
            )
        connection.commit()
        return JSONResponse(content={"message": "Log registered successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()