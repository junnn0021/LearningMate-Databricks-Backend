from fastapi import APIRouter, Request
from app.translate import translate_naveropenapi
from app.ai.ai_serve import serve_completion
from fastapi.responses import JSONResponse
from app.routers.statistics_routers import *
import json
import re

router = APIRouter(
    prefix="/databricks",
)

@router.get("/question")
async def question():
    return {"msg:this is databricks question"}


@router.post("/question2")
async def question2():
    return {"msg:this is databricks question2"}

#AI server
@router.post("/ai")
async def ai_serve(request: Request):
    data = await request.json()
    request_msg = data.get("request")
    request_ip = data.get("request_ip")
    print("넣고자 하는 msg: {0}". format(request_msg))
    print("넣고자 하는 ip: {0}". format(request_ip))

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

    if re.search(r"영화", request_msg):
        try:
            ## DB 넣을 AI 연결
            # completion_result_db = text_contest  ## DB에 넣는 목적의 데이터로 변환
            completion_result_db = serve_completion(request_msg, 1)  ## DB에 넣는 목적의 데이터로 변환
            print("DB에 데이터 넣는 목적 AI 결과 : {0}".format(completion_result_db))

            # JSON 데이터를 파싱하여 변수에 저장
            response_split_json = completion_result_db.split("```")[1].split("```")[0].strip()
            response_data = json.loads(response_split_json, strict=False)
            print("response_data : {0}".format(response_data))

            # ai_movie_info 테이블에 데이터 자장
            await save_ai_movie_info_call(response_data)

            # ai_movie_request 테이블에 데이터 저장
            await ai_movie_request_call(request_msg, request_ip)

        except Exception as e:
            return JSONResponse(content={"message": e}, status_code=404)

    try:
        ## Front 단으로 넘길 AI 연결
        completion_result_front = serve_completion(request_msg, 2)  ## Front 단으로 전송하기 위한 데이터로 변환
        completion_result_front_ko = translate_naveropenapi(source="en", target="ko", sentence=completion_result_front)
        print("front에 반환하는 목적 AI 결과 : {0}".format(completion_result_front_ko))

    except Exception as e:
        return JSONResponse(status_code=404, content={"result": e})

    return JSONResponse(status_code=200, content={"result": text_contest})
    ## 임시 주석
    return JSONResponse(status_code=200, content={"result": request_test_contxt})

# ai_movie_request 테이블에 데이터 저장
async def ai_movie_request_call(param_request_msg, param_request_ip):

    movie_data = AiMovieRequest(
        ai_request_text=param_request_msg,
        request_ip=param_request_ip
    )

    print("post_request_data : {0}".format(movie_data))
    await save_ai_movie_request_call(movie_data)


# save_ai_movie_info 테이블에 데이터 저장
async def save_ai_movie_info_call(data):

    for movie in data:
        movie_data = AiMovieInfo(
            ai_movie_info_id=11,  # 필수 필드 추가
            ai_movie_response_id=11,
            movie_title=translate_naveropenapi(source="en", target="ko", sentence=movie['title']),
            movie_genre=translate_naveropenapi(source="en", target="ko", sentence=movie['genre']),
            movie_actor=translate_naveropenapi(source="en", target="ko", sentence=movie['actors']),
            movie_year=int(movie['year']),
            movie_nation=translate_naveropenapi(source="en", target="ko", sentence=movie['nation']),
            movie_director=translate_naveropenapi(source="en", target="ko", sentence=movie['director']),
            movie_age= int(movie['recommended_age'].replace("+", "")),
            movie_story=translate_naveropenapi(source="en", target="ko", sentence=movie['plot']),
            reg_dt=datetime.now().isoformat()  # 문자열로 변환
        )
        await save_ai_movie_info(movie_data)

    print("post_request_data : {0}".format(movie_data))


#민수님 call test
test_content = """기꺼이 영화를 추천하겠습니다. 다양한 장르를 기반으로 몇 가지 제안 사항을 소개합니다:

**액션/스릴러:**
* '미션: 임파서블 - 폴아웃'(2018)은 놀라운 스턴트와 흥미진진한 줄거리를 가진 하이옥탄 스파이 스릴러입니다.
* '존 윅: 챕터 3 - 파라벨룸'(2019) - 아드레날린을 자극하는 액션 영화로, 전투 안무가 인상적입니다.

**로맨스:**
* '수첩'(2004)은 수십 년에 걸친 아름다운 러브 스토리를 담은 고전 로맨틱 드라마입니다.
* '라라 랜드'(2016)는 멋진 공연과 매혹적인 사운드트랙이 돋보이는 현대 로맨틱 뮤지컬입니다.

**공상 과학 소설:**
* '블레이드 러너 2049'(2017)는 생각을 자극하는 서사를 담은 시각적으로 놀라운 공상과학 서사시입니다.
* '어라이벌'(2016)은 독특한 시간 여행 콘셉트의 놀라운 공상과학 영화입니다.

**코미디:**
* '행오버'(2009)는 라스베이거스의 거친 밤을 다룬 유쾌하고 거친 코미디입니다.
* '그랜드 부다페스트 호텔'(2014)은 독특한 스토리라인을 갖춘 기발하고 시각적으로 멋진 코미디 드라마입니다."""
@router.post("/ai-nocall")
async def ai_serve_test():
    return JSONResponse(status_code=200, content={"result":test_content})

