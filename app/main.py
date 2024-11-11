from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from app.ai.ai_serve import *

from app.routers import databricks_routers
from app.routers import statistics_routers
from fastapi.middleware.cors import CORSMiddleware

# 환경변수 세팅 (.env 파일생성필요)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# set_env()
app = FastAPI()
app.include_router(databricks_routers.router)
app.include_router(statistics_routers.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test01():
    return {"Hello": "Junseok World."}


@app.get("/ ")
def translate():
    from app.translate import run_translate_ko_to_en
    # sentence = "우크라이나 대통령실이 러시아와 전쟁이 끝난 직후 대통령 선거를 치를 것이라고 밝혔다고 우크라이나 매체 키이우인디펜던트와 우크라인스카프라우다가 27일(현지시간) 보도했다."
    # >> {"message":"Ukraine's presidential office said it would hold a presidential election shortly after the war with Russia, Ukrainian media Kyiv Independent and Ukraine's Scafrauda reported on the 27th (local time)."}
    # sentence = "한국 영화 중에 슬픈영화 10가지 알려줘"
    sentence = "Tell me 10 sad Korean movies"
    print("sent : {}", sentence)
    # msg = run_translate_ko_to_en(source="ko",target="en",sentence=sentence)
    msg = run_translate_ko_to_en(source="en",target="ko",sentence=sentence)
    return {"message":msg}

#AI server
@app.post("/ai")
async def ai_serve(request: Request):
    # request = "Recommend marvel movies with ratdings and director and plot. "
    data = await request.json()
    request_msg = data.get("request")
    request_ip = data.get("request_ip")
    print("request_msg : {0}". format(request_msg))
    completion_result= serve_completion(request_msg)
    print("AI 결과 : {0}". format(completion_result))
    if completion_result:
        # JSON 데이터를 파싱하여 변수에 저장

        response_split_json = completion_result.split("```")[1].split("```")[0].strip()
        data = json.loads(response_split_json, strict=False)

        # 오브젝트 변수를 새로 만들고, 변환할 것 변환 한 다음 리스트에 저장
        output_list_value = []
        for movie in data:
            movie_data = {
                "Title": movie['title'],
                "Rating": movie['rating'],
                "Actors": movie['actors'],
                "Director": movie['director'],
                "Plot": movie['plot'],
                "Plot_trans": run_translate_ko_to_en(source="en", target="ko", sentence=movie['plot'])
            }
            output_list_value.append(movie_data)

        ## DB insert 부분 추가 필요

        # JSON 재 변환 후 반환
        json_data = json.dumps(output_list_value, ensure_ascii=False)

        # 성공 후 요청 질문 DB insert를 하는 프로시저 호출 테스트
        post_request_data = {
            "ai_request_text": request_msg,
            "ai_request_id": 15,
            "request_ip": request_ip
        }
        print("post_request_data : {0}".format(post_request_data))
        save_ai_movie_request_call_procedure(post_request_data)

        return JSONResponse(content={"message": "Databricks 200", "result": json_data})

    else:
        return JSONResponse(content={"message": "server not found"}, status_code=404)

#민수님 call test
@app.post("/ai-nocall")
async def ai_serve_test():
    return JSONResponse(status_code=200, content={"message": "Databricks 200", "result": "minsoo"})