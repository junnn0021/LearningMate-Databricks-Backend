from openai import OpenAI
import os
from dotenv import load_dotenv
 
# 환경변수 세팅 (.env 파일생성필요)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def serve_completion(request):
    client = OpenAI(
        api_key=os.environ["TOKEN"],
        base_url=os.environ["ENDPOINT"]
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant"
            },
            {
                "role": "user",
                "content": request
            }
        ],
        model="devops3_serving",
        max_tokens=8000
    )
    return chat_completion.choices[0].message.content