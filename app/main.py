from fastapi import FastAPI, Depends, Response
from app.ai.ai_serve import *
from app.db.ai_movie_request import *

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
def health_check():
    return {"Hello": "Junseok World."}
