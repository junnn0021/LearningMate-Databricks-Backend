import pymysql
import os
from dotenv import load_dotenv
 
# 환경변수 세팅 (.env 파일생성필요)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
 
 
def get_db_connection():
    connection = pymysql.connect(
        host=os.environ["HOST"],
        port=int(os.environ["PORT"]),
        user=os.environ["USER"],
        password=os.environ["PASSWORD"],
        database=os.environ["DATABASE"],
    )
    return connection