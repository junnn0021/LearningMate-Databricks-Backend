from fastapi.responses import JSONResponse
from app.db_connection import get_db_connection
from app.models import AiMovieResponseReview

def ai_movie_review_call_procedure(review_data: AiMovieResponseReview):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(
                'usp_ai_review_I',
                (
                    review_data.ai_response_id,
                    review_data.ai_user_review,
                    review_data.ai_user_score,
                    review_data.ai_review_id,
                )
            )
            result = cursor.fetchall()
        connection.commit()
        return JSONResponse(content={"message": "Review registered successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()