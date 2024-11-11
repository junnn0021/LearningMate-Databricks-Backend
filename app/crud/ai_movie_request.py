from fastapi.responses import JSONResponse
from app.db_connection import get_db_connection
from app.models import AiMovieRequest

def save_ai_movie_request_call_procedure(request_data: AiMovieRequest):
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