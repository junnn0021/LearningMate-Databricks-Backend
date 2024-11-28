from fastapi import FastAPI,APIRouter, Request
from app.translate import translate_naveropenapi
from app.ai.ai_serve import serve_completion
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from app.routers.statistics_routers import *

import json
import re
import requests

app = FastAPI()
router = APIRouter(
    prefix="/databricks",
)

@router.get("/health")
async def question():
    return {"msg:success health check"}


@router.post("/ai")
async def ai_serve(request: Request):
    text_contest = '''
    Here are 2 SF movie recommendations in plain text format and JSON object format:

**Plain Text Format:**

1. **Inception (2010)**
	* Rating: 8.8/10
	* Actors: Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page, Tom Hardy
	* Director: Christopher Nolan
	* Plot: A team of thieves must plant an idea in someone's mind instead of stealing it, using shared dreaming technology.
2. **Interstellar (2014)**
	* Rating: 8.1/10
	* Actors: Matthew McConaughey, Anne Hathaway
	* Director: Christopher Nolan
	* Plot: A team of astronauts travels through a wormhole in search of a new habitable planet for humanity, facing challenges such as gravitational forces and time dilation.

**JSON Object Format:**

```
[
  {
    "title": "Inception",
    "year": 2010,
    "nation": "USA",
    "genre": "Science Fiction, Action, Thriller",
    "actors": "Leonardo DiCaprio, Joseph Gordon-Levitt",
    "director": "Christopher Nolan",
    "recommended_age": "18+",
    "plot": "A team of thieves must plant an idea in someone's mind instead of stealing it, using shared dreaming technology."
  },
  {
    "title": "Interstellar",
    "year": 2014,
    "nation": "USA",
    "genre": "Science Fiction, Adventure, Drama",
    "actors": "Matthew McConaughey, Anne Hathaway",
    "director": "Christopher Nolan",
    "recommended_age": "14+",
    "plot": "A team of astronauts travels through a wormhole in search of a new habitable planet for humanity, facing challenges such as gravitational forces and time dilation."
  }
]
```
    '''    
    # data = await request.json()
    # # print(f"data: {data}") #  {'request': '경훈 액션 영화 추천 부탁해', 'request_ip': '127.0.0.1'}
    # request_msg = data.get("request")
    # request_ip = data.get("request_ip")
    request_msg="영화 2편 추천해줘"
    request_ip="127.1.1"
    if re.search(r"영화", request_msg):
        try:
            # completion_result_db = serve_completion(request_msg, 1) # 데이터 브릭스 API 호출하기
            text_plain = text_contest.split("**JSON Object Format:**")[0].strip()
            response_split_json = text_contest.split("```")[1].split("```")[0].strip() # 테스트 데이터 서용
            response_data = json.loads(response_split_json, strict=False)


            # 1. ai_movie_request 테이블에 데이터 저장
            ai_movie_request = AiMovieRequest(
                ai_request_text=request_msg,
                request_ip=request_ip
            )
            req_response = await save_ai_movie_request_call(ai_movie_request)
            req_response_data = json.loads(req_response.body.decode('utf-8'))
            ai_movie_req_result_id = str(req_response_data.get("result_id"))
            print(f"ai_movie_req_result_id: {ai_movie_req_result_id}")
            

            # 2.ai_movie_response 테이블에 데이터 저장
            ai_movie_response = AiMovieResponse(
                ai_request_id=ai_movie_req_result_id,
                ai_response_text=text_contest,
                ai_response_time=99,
                ai_response_model='llama3.1',
            )
            # print(f"ai_movie_response\n:{ai_movie_response}")
            res_response = await save_ai_movie_response_call(ai_movie_response)
            dict_response_data = json.loads(res_response.body.decode('utf-8'))
            ai_movie_res_result_id = str(dict_response_data.get("result_id"))
            print(f"ai_movie_res_result_id: {ai_movie_res_result_id}")
            # print(response_data)


            # 3.ai_movie_info 테이블에 데이터 저장
            for movie in response_data:
                movie_data = AiMovieInfo(
                    ai_movie_response_id=int(ai_movie_res_result_id),
                    movie_title=translate_naveropenapi(source="en", target="ko", sentence=movie['title']),
                    movie_genre=translate_naveropenapi(source="en", target="ko", sentence=movie['genre']),
                    movie_actor=translate_naveropenapi(source="en", target="ko", sentence=movie['actors']),
                    movie_year=int(movie['year']),
                    movie_nation=translate_naveropenapi(source="en", target="ko", sentence=movie['nation']),
                    movie_director=translate_naveropenapi(source="en", target="ko", sentence=movie['director']),
                    movie_age=movie['recommended_age'],
                    movie_story=translate_naveropenapi(source="en", target="ko", sentence=movie['plot']),
                    reg_dt=datetime.now().isoformat()
                )
                response = await save_ai_movie_info_call(movie_data)
                response_data = json.loads(response.body.decode('utf-8'))
                print("response : {0}".format(str(response_data.get("result_id"))))

            print(str(response_data.get("result_id")))
            
        except Exception as e:
            return JSONResponse(content={"message": e}, status_code=404)

    try:
        ## Front 단으로 넘길 AI 연결
        #completion_result_front = serve_completion(request_msg, 2)  ## Front 단으로 전송하기 위한 데이터로 변환
        completion_result_front_ko = translate_naveropenapi(source="en", target="ko", sentence=text_plain)
        print("front에 반환하는 목적 AI 결과 : {0}".format(completion_result_front_ko))

    except Exception as e:
        return JSONResponse(status_code=404, content={"result": e})

    return JSONResponse(status_code=200, content={"result": completion_result_front_ko})        
    
