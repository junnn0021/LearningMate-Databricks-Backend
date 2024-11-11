from fastapi.responses import JSONResponse
from app.db_connection import get_db_connection

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