from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field  


class AiMovieLog(BaseModel):
    log_id: int  # bigint NOT
    log_type: str  # varchar(10)
    log_msg: str  # text NOT
    log_time: datetime  # datetime NOT
    log_name: str  # varchar(45
    function_name: str  # varchar(45
    line_no: int  # int DEFAULT
    process_id: str  # varchar(45
    process_name: str  # varchar(45
    thread_id: str  # varchar(45
    thread_name: str  # varchar(45
    work_name: str  # varchar(45
    stack: str  # text COMMENT
    path: str  # varchar(255

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "log_id": "temp",  # 로그아이디
                    "log_type": "temp",  # 로그유형(DEBUG, INFO, WARNING, ERROR, CRITICAL)
                    "log_msg": "temp",  # ,로그 메세지
                    "log_time": "temp",  # 로그 시간
                    "log_name": "temp",  # 로그명
                    "function_name": "temp",  # 함수명
                    "line_no": "temp",  # 줄번호
                    "process_id": "temp",  # 프로세스 아이디
                    "process_name": "temp",  # 프로세스명
                    "thread_id": "temp",  # 쓰레드 아이디
                    "thread_name": "temp",  # 쓰레드명
                    "work_name": "temp",  # 작업명
                    "stack": "temp",  # 스택
                    "path": "temp",  # 경로
                }
            ]
        }
    }


class AiMovieRequest(BaseModel):
    # ai_request_id: int  # bigint NOT
    ai_request_id: Optional[int] = Field(default=None)
    ai_request_text: str  # text
    ai_request_time: str  # datetime
    request_ip: str  # varchar(15)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    # "ai_request_id": "temp",  # 로그아이디
                    "ai_request_id": None,
                    "ai_request_text": "액션 영화 추천 부탁해",  # 추천요청 내용
                    "ai_request_time": "temp",  # 추천요청시간
                    "request_ip": "temp",  # 요청IP
                }
            ]
        }
    }


class AiMovieResponse(BaseModel):
    ai_response_id: Optional[int] = Field(default=None)
    # ai_response_id: int  # bigint NOT
    ai_request_id: str  # bigint NOT
    ai_response_text: str  # text
    ai_response_time: int  # int
    movie_title: str  # varchar(45)
    movie_year: int  # varchar(45)
    movie_genre: str  # varchar(45)
    movie_director: str  # varchar(45)
    movie_actor: str  # varchar(255)
    movie_nation: str  # varchar(45)
    movie_age: int  # varchar(45)
    movie_story: str  # text
    ai_response_model: str  # varchar(45)
    reg_dt: datetime  # datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ai_response_id": None,  # 로그아이디
                    "ai_request_id": "temp",  # 추천요청 내용
                    "ai_response_text": "temp",  # 추천요청시간
                    "ai_response_time": "temp",  # 요청IP
                    "movie_title": "temp",  # 요청IP
                    "movie_year": "temp",  # 요청IP
                    "movie_genre": "temp",  # 요청IP
                    "movie_director": "temp",  # 요청IP
                    "movie_actor": "temp",  # 요청IP
                    "movie_nation": "temp",  # 요청IP
                    "movie_age": "temp",  # 요청IP
                    "movie_story": "temp",  # 요청IP
                    "ai_response_model": "temp",  # 요청IP
                    "reg_dt": "temp",  # 요청IP
                }
            ]
        }
    }


class AiMovieResponseReview(BaseModel):
    ai_review_id: int  # bigint
    ai_response_id: int  # bigint
    ai_user_review: str  # varchar(255)
    ai_user_score: int  # int
    # reg_dt: datetime  # datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ai_review_id": "temp",  # 리뷰아이디
                    "ai_response_id": "temp",  # 추천응답 아이디
                    "ai_user_review": "흥미진진하다",  # 사용자 리뷰 내용
                    "ai_user_score": "5",  # 사용자 점수
                    # "reg_dt": "temp",  # 등록일시
                }
            ]
        }
    }


class AiMovieStatics(BaseModel):
    ai_statics_id: int  # bigint
    ai_statics_type: str  # varchar(45)
    ai_statics_value: str  # varchar(45)
    ai_statics_count: int  # int
    ai_statics_day: str  # varchar(10)
    reg_dt: datetime  # datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ai_statics_id": "temp",  # 통계아이디
                    "ai_statics_type": "temp",  # 통계유형(검색량,제공영화수,영화제목,영화년도, 영화장르, 영화감독, 영화배우, 영화국가, 영화년도)
                    "ai_statics_value": "temp",  #
                    "ai_statics_count": "temp",  # 통계수
                    "ai_statics_day": "temp",  #
                    "reg_dt": "temp",  # 등록일시
                }
            ]
        }
    }
