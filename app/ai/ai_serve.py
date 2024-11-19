from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from app.translate import translate_naveropenapi

# 환경변수 세팅 (.env 파일생성필요)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def serve_completion(request, type):

    msg = translate_naveropenapi(source="ko",target="en",sentence=request)
    print("한글을 영문으로 변경: {}".format(msg))

    """
    msg 예시(영문) : Please recommend 10 SF movies with ratings, actor, directors and plotlines. 
    msg 예시(한글) : 평점, 배우, 감독, 줄거리가 있는 SF 영화 10편을 추천해 주세요. 
    
    """
    client = OpenAI(
        api_key=os.environ["TOKEN"],
        base_url=os.environ["ENDPOINT"]
    )

    if type == 1:
        ai_request_format = "You are an AI assistant, Please translate the answer provide the response in plain text format and into Json object format as a list {[{'title': '', 'year':'' ,'nation': '', 'genre': '', 'actors': '', 'director': '', 'recommended_age' : '', 'plot(plot should not have any quotes.)': '']}"
    else:
        ai_request_format = "You are an AI assistant, Please translate the answer provide the response in plain text format"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": ai_request_format
            },
            {
                "role": "user",
                "content": msg
             }
        ],
        model="devops3_serving",
        max_tokens=8000
    )
    return chat_completion.choices[0].message.content