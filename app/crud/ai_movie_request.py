from fastapi.responses import JSONResponse
from app.db_connection import get_db_connection
from app.models import AiMovieRequest

def save_ai_movie_request_call_procedure(request_data: AiMovieRequest):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_request_I', 
                (request_data.ai_request_text, request_data.ai_request_time, request_data.request_ip)
            )
            result = cursor.fetchall()
        connection.commit()
        return JSONResponse(content={"message": "Request saved successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()