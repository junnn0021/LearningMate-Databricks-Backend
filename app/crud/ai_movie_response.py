from fastapi.responses import JSONResponse
from app.db_connection import get_db_connection
from app.models import AiMovieResponse

async def save_ai_movie_response_call_procedure(response_data: AiMovieResponse):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'ai_movie.usp_ai_movie_response_I',
                (
                    response_data.ai_request_id,
                    response_data.ai_response_text,
                    response_data.ai_response_time,
                    response_data.movie_title,
                    response_data.movie_year,
                    response_data.movie_genre,
                    response_data.movie_director,
                    response_data.movie_actor,
                    response_data.movie_nation,
                    response_data.movie_age,
                    response_data.movie_story,
                    response_data.ai_response_model,
                    response_data.reg_dt,
                )
            )
            result_id = cursor.fetchone()[0]
        connection.commit() 
        return JSONResponse(content={"message": "Response saved successfully", "result_id": result_id}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close() 
