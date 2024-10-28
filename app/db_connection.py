import pymysql
import os
# from dotenv import load_dotenv
 
 
def get_db_connection():
    connection = pymysql.connect(
        host=os.environ["HOST"],
        port=int(os.environ["PORT"]),
        user=os.environ["USER"],
        password=os.environ["PASSWORD"],
        database=os.environ["DATABASE"],
    )
    return connection
