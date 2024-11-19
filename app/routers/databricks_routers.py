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

    if re.search(r"영화", request_msg):
        try:
            ## DB 넣을 AI 연결
            completion_result_db = serve_completion(request_msg, 1)  ## DB에 넣는 목적의 데이터로 변환
            print("DB에 데이터 넣는 목적 AI 결과 : {0}".format(completion_result_db))

            # JSON 데이터를 파싱하여 변수에 저장
            response_split_json = completion_result_db.split("```")[1].split("```")[0].strip()
            data = json.loads(response_split_json, strict=False)

            # 오브젝트 변수를 새로 만들고, 변환할 것 변환 한 다음 리스트에 저장
            output_list_value = []
            for movie in data:
                movie_data = {
                    "title": movie['title'],
                    "nation": movie['nation'],
                    "genre": movie['genre'],
                    "actors": movie['actors'],
                    "director": movie['director'],
                    "recommended_age": movie['recommended_age'],
                    "Plot": movie['plot'],
                    "Plot_trans": translate_naveropenapi(source="en", target="ko", sentence=movie['plot'])
                }
                output_list_value.append(movie_data)

            ## DB insert 부분 추가 필요
            # JSON 재 변환 후 반환
            json_data = json.dumps(output_list_value, ensure_ascii=False)

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

    return JSONResponse(status_code=200, content={"result": completion_result_front_ko})
    ## 임시 주석
    return JSONResponse(status_code=200, content={"result": request_test_contxt})

## 주석처리
# async def ai_serve(request: Request):
#     request_test_contxt = """
#             Here are two SF movie recommendations with ratings, actors, directors, and plotlines:
#
#         **Movie 1: Blade Runner (1982)**
#
#         * **Rating:** 8.5/10
#         * **Actors:** Harrison Ford, Rutger Hauer, Sean Young
#         * **Director:** Ridley Scott
#         * **Plot:** In a dystopian future, a special police officer (Harrison Ford) is tasked with tracking down advanced androids known as replicants. As he delves deeper into the case, he begins to question the nature of humanity and his own existence.
#
#         **Movie 2: Inception (2010)**
#
#         * **Rating:** 8.8/10
#         * **Actors:** Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page
#         * **Director:** Christopher Nolan
#         * **Plot:** A skilled thief (Leonardo DiCaprio) is hired to perform a task known as "inception" - planting an idea in someone's mind instead of stealing one. As he assembles a team of experts, they must navigate the blurred lines between reality and dreams to achieve their goal.
#
#         Here is the response in JSON object format as a list:
#
#         ```
#         [
#           {
#             "title": "Blade Runner",
#             "nation": "USA",
#             "genre": "Science Fiction",
#             "actors": "Harrison Ford, Rutger Hauer, Sean Young",
#             "director": "Ridley Scott",
#             "recommended_age": "18+",
#             "plot": "In a dystopian future, a special police officer is tasked with tracking down advanced androids known as replicants. As he delves deeper into the case, he begins to question the nature of humanity and his own existence."
#           },
#           {
#             "title": "Inception",
#             "nation": "USA",
#             "genre": "Science Fiction, Action",
#             "actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page",
#             "director": "Christopher Nolan",
#             "recommended_age": "17+",
#             "plot": "A skilled thief is hired to perform a task known as inception - planting an idea in someone's mind instead of stealing one. As he assembles a team of experts, they must navigate the blurred lines between reality and dreams to achieve their goal."
#           }
#         ]
#         ```
#     """
#     data = await request.json()
#     request_msg = data.get("request")
#     request_ip = data.get("request_ip")
#     print("넣고자 하는 msg: {0}". format(request_msg))
#     print("넣고자 하는 ip: {0}". format(request_ip))
#
#     if re.search(r"영화", request_msg):
#         try:
#             ## DB 넣을 AI 연결
#             #completion_result_db = serve_completion(request_msg, 1)  ## DB에 넣는 목적의 데이터로 변환
#             completion_result_db = request_test_contxt  ## DB에 넣는 목적의 데이터로 변환 - 임시 데이터 더미
#             print("DB에 데이터 넣는 목적 AI 결과 : {0}".format(completion_result_db))
#
#             # JSON 데이터를 파싱하여 변수에 저장
#             response_split_json = completion_result_db.split("```")[1].split("```")[0].strip()
#             data = json.loads(response_split_json, strict=False)
#
#             # 오브젝트 변수를 새로 만들고, 변환할 것 변환 한 다음 리스트에 저장
#             output_list_value = []
#             for movie in data:
#                 movie_data = {
#                     "title": movie['title'],
#                     "nation": movie['nation'],
#                     "genre": movie['genre'],
#                     "actors": movie['actors'],
#                     "director": movie['director'],
#                     "recommended_age": movie['recommended_age'],
#                     "Plot": movie['plot'],
#                     # "Plot_trans": translate_naveropenapi(source="en", target="ko", sentence=movie['plot'])
#                 }
#                 output_list_value.append(movie_data)
#
#             ## DB insert 부분 추가 필요
#             # JSON 재 변환 후 반환
#             json_data = json.dumps(output_list_value, ensure_ascii=False)
#
#             # ai_movie_request 테이블에 데이터 저장
#             await ai_movie_request_call(request_msg, request_ip)
#
#         except Exception as e:
#             return JSONResponse(content={"message": e}, status_code=404)
#
#     # try:
#     #     ## Front 단으로 넘길 AI 연결
#     #     completion_result_front = serve_completion(request_msg, 2)  ## Front 단으로 전송하기 위한 데이터로 변환
#     #     completion_result_front_ko = translate_naveropenapi(source="en", target="ko", sentence=completion_result_front)
#     #     print("front에 반환하는 목적 AI 결과 : {0}".format(completion_result_front_ko))
#     #
#     # except Exception as e:
#     #     return JSONResponse(status_code=404, content={"result": e})
#     #
#     # return JSONResponse(status_code=200, content={"result": completion_result_front_ko})
#     ## 임시 주석
#     return JSONResponse(status_code=200, content={"result": request_test_contxt})


# ai_movie_request 테이블에 데이터 저장
async def ai_movie_request_call(param_request_msg, param_request_ip):

    movie_data = AiMovieRequest(
        ai_request_text=param_request_msg,
        request_ip=param_request_ip
    )

    print("post_request_data : {0}".format(movie_data))
    await save_ai_movie_request_call(movie_data)


# save_ai_movie_info 테이블에 데이터 저장
async def save_ai_movie_info_call(param_request_msg, param_request_ip):

    movie_data = AiMovieInfo(
        ai_movie_info_id = int,
        ai_movie_response_id = int,
        movie_title = str,
        movie_genre = str,
        movie_actor = str,
        movie_year = int,
        movie_nation = str,
        movie_age = int,
        movie_story = str,
        reg_dt = str,
    )

    print("post_request_data : {0}".format(movie_data))
    await save_ai_movie_info(movie_data)
