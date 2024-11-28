import pymysql
import os
# from dotenv import load_dotenv

def get_db_connection():
    connection = pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ["PORT"]),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
    )
    return connection
