from fastapi import APIRouter

router = APIRouter(
    prefix="/statistics",
)

@router.get("/test1")
def test1():
    # 1. 비즈니스 로직 호출 (기존 생성 함수)
    return {"msg:this is statistics router test1"}

@router.get("/test2")
def test2():
    return {"msg:this is statistics router test2"}


@router.get("/test3")
def test3():
    return {"msg:this is statistics router test3"}


@router.get("/test4")
def test4():
    return {"msg:this is statistics router test4"}

"""
아래 로직을 라우터에 적용하면 됩니다.

# junseok MYSQL call procedure
@app.post("/movie/log/call")
async def save_ai_movie_log_call(log_data: AiMovieLog):
    return ai_movie_log_call_procedure(log_data)

@app.post("/movie/request/call3")
async def save_ai_movie_request_call(request_data: AiMovieRequest):
    return ai_movie_request_call_procedure3(request_data)

@app.post("/movie/response/call")
async def save_ai_movie_response_call(response_data: AiMovieResponse):
    return await ai_movie_response_call_procedure(response_data)

@app.post("/movie/review/call")
async def save_movie_review_call(review_data: AiMovieResponseReview):
    return ai_movie_review_call_procedure(review_data)

"""