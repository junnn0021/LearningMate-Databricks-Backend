from app.crud.ai_movie_log import save_ai_movie_log_call_procedure
from app.crud.ai_movie_request import save_ai_movie_request_call_procedure
from app.crud.ai_movie_response import save_ai_movie_response_call_procedure
from app.crud.ai_movie_response_review import ai_movie_review_call_procedure
from app.crud.ai_movie_statics import *
from app.models import *
from fastapi import APIRouter


router = APIRouter(
    prefix="/statistics",
)

@router.post("/log")
async def save_ai_movie_log_call(log_data: AiMovieLog):
    return save_ai_movie_log_call_procedure(log_data)

@router.post("/request")
async def save_ai_movie_request_call(request_data: AiMovieRequest):
    return save_ai_movie_request_call_procedure(request_data)

@router.post("/response")
async def save_ai_movie_response_call(response_data: AiMovieResponse):
    return await save_ai_movie_response_call_procedure(response_data)

@router.post("/review")
async def save_movie_review_call(review_data: AiMovieResponseReview):
    return ai_movie_review_call_procedure(review_data)

@router.get("/movie_actor")
async def get_movie_statics_movie_actor_call():
    return get_movie_statics_movie_actor_call_procedure()

@router.get("/movie_count")
async def get_movie_statics_movie_count_call():
    return get_movie_statics_movie_count_call_procedure()

@router.get("/movie_genre")
async def get_movie_statics_movie_genre_call():
    return get_movie_statics_movie_genre_call_procedure()

@router.get("/movie_title")
async def get_movie_statics_movie_title_call():
    return get_movie_statics_movie_title_call_procedure()

@router.get("/request_count")
async def get_movie_statics_request_count_call():
    return get_movie_statics_request_count_call_procedure()

@router.get("/user_score")
async def get_movie_statics_user_score_call():
    return get_movie_statics_user_score_call_procedure()