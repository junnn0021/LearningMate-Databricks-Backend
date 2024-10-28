from openai import OpenAI
import os
from dotenv import load_dotenv
from app.translate import run_translate_ko_to_en

# 환경변수 세팅 (.env 파일생성필요)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def serve_completion(request):

    msg = run_translate_ko_to_en(source="ko",target="en",sentence=request)
    print("msg : {}".format(msg))

    client = OpenAI(
        api_key=os.environ["TOKEN"],
        base_url=os.environ["ENDPOINT"]
    )

    print("api_key : "+ os.environ["TOKEN"])
    print("base_url : "+ os.environ["ENDPOINT"])
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant"
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