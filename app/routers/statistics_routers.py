from app.db.ai_movie_request import save_ai_movie_request_call_procedure
from app.db.call_db_procedure import call_db_procedure
from app.models import *
from fastapi import APIRouter


router = APIRouter(
    prefix="/statistics",
)

@router.post("/info")
async def save_ai_movie_info(movie_data: AiMovieInfo):
    args = (
        movie_data.ai_movie_info_id,
        movie_data.ai_movie_response_id,
        movie_data.movie_title,
        movie_data.movie_genre,
        movie_data.movie_actor,
        movie_data.movie_year,
        movie_data.movie_nation,
        movie_data.movie_age,
        movie_data.movie_story,
        movie_data.movie_director,
        movie_data.reg_dt
    )
    return await call_db_procedure('usp_ai_movie_info_I', args)

@router.post("/log")
async def save_ai_movie_log_call(log_data: AiMovieLog):
    args = (
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
    return await call_db_procedure('usp_ai_movie_log_I', args)

@router.post("/request")
async def save_ai_movie_request_call(request_data: AiMovieRequest):
    return save_ai_movie_request_call_procedure(request_data)

@router.post("/response")
async def save_ai_movie_response_call(response_data: AiMovieResponse):
    args = (
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
    return await call_db_procedure('ai_movie.usp_ai_movie_response_I', args)

@router.post("/review")
async def save_movie_review_call(review_data: AiMovieResponseReview):
    args = (
        review_data.ai_response_id,
        review_data.ai_user_review,
        review_data.ai_user_score,
        review_data.ai_review_id,
    )
    return await call_db_procedure('usp_ai_review_I', args)


@router.get("/movie_actor")
async def get_movie_statics_movie_actor_call():
    return await call_db_procedure('ai_movie.usp_ai_movie_statics_movie_actor_L', ())

@router.get("/movie_count")
async def get_movie_statics_movie_count_call():
    return await call_db_procedure('ai_movie.usp_ai_movie_statics_movie_count_L', ())

@router.get("/movie_genre")
async def get_movie_statics_movie_genre_call():
    return await call_db_procedure('ai_movie.usp_ai_movie_statics_movie_genre_L', ())

@router.get("/movie_title")
async def get_movie_statics_movie_title_call():
    return await call_db_procedure('ai_movie.usp_ai_movie_statics_movie_title_L', ())

@router.get("/request_count")
async def get_movie_statics_request_count_call():
    return await call_db_procedure('ai_movie.usp_ai_movie_statics_request_count_L', ())

@router.get("/user_score")
async def get_movie_statics_user_score_call():
    return await call_db_procedure('ai_movie.usp_ai_movie_statics_user_score_L', ())
