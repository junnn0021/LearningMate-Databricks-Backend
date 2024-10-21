from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from typing import Optional, Union, List, Any
from fastapi import FastAPI
from db_connection import get_db_connection
from db.ai_movie_log import *
from db.ai_movie_request import *
from db.ai_movie_response import *
from db.ai_movie_response_review import *
from db.ai_movie_statics import *
from ai.ai_serve import *
from models import AiMovieRequest

app = FastAPI()


# 전체 리스트 조회
@app.get("/test", response_model=list[AiMovieRequest])
def test() -> list[AiMovieRequest]:
    """
    쿼리 프로세스 설명
    1. QUERY(SELECT)
    2. MAKE ARRAY JSON DATA(Header + Rows)
    3. RETURN JSONResponse
    4. Validate Pydantic model
    5. Return Pydantic model
        - with json Response data
    """
    mapping = []
    response = []
    connection = get_db_connection()
    cursor = connection.cursor()
    query = f"""
    select 
        ai_request_id
        , ai_request_text
        , DATE_FORMAT(ai_request_time, '%Y-%m-%d %h:%m:%s') as ai_request_time
        , request_ip
    from ai_movie_request
    """
    cursor.execute(query)
    col_headers = [x[0] for x in cursor.description]
    rows = cursor.fetchall()
    # print(col_headers) # ['ai_request_id', 'ai_request_text', 'ai_request_time', 'request_ip']
    # print(rows)
    for result in rows:
        mapping.append(dict(zip(col_headers, result)))

    for x in mapping:
        print(x)
        response.append(
            AiMovieRequest(
                ai_request_id=x.get("ai_request_id"),
                ai_request_text=x.get("ai_request_text"),
                ai_request_time=x.get("ai_request_time"),
                request_ip=x.get("request_ip"),
            )
        )

    return response


@app.get("/")
def read_root():
    return {"Hello": "Junseok World."}


# MYSQL biz
@app.get("/movie/log/select")
def movie_log_select():
    return ai_movie_log_select()


@app.get("/movie/request/select")
def movie_request_select():
    return ai_movie_request_select()


@app.get("/movie/response/select")
def movie_response_select():
    return ai_movie_response_select()


# MYSQL call procedure
@app.get("/movie/request/call")
def movie_request_call_procedure():
    return ai_movie_request_call_procedure("call1", "2024-10-17", 1)


@app.get("/movie/request/call2")
def movie_request_call_procedure2():
    return ai_movie_request_call_procedure2("call2", "2024-10-17", 10)


# AI server
@app.get("/ai")
async def ai_serve(request: str):
    request = "Recommend marvel movies with ratdings and director and plot. "
    result = serve_completion(request)
    print(result)
    if result:
        return JSONResponse(content={"message": "serve found", "result": result})
    else:
        return JSONResponse(content={"message": "server not found"}, status_code=404)


# TEST
@app.get("/test-db")
def test_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM new_schema.new_table")
    result = cursor.fetchall()
    connection.close()

    result = [(str(row[0]), row[1]) for row in result]

    return JSONResponse(
        content={"message": "Database connection successful", "result": result}
    )


@app.post("/items")
async def create_item(id: int, first_name: str, last_name: str, email: str, hire: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO new_table (id, first_name, last_name, email, hire) VALUES (%s, %s, %s, %s, %s)",
        (id, first_name, last_name, email, hire),
    )
    connection.commit()
    connection.close()
    return JSONResponse(
        content={"message": "Item created successfully"}, status_code=201
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM new_table WHERE id = %s", (item_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        result = (str(result[0]), result[1])
        return JSONResponse(content={"message": "Item found", "result": result})
    else:
        return JSONResponse(content={"message": "Item not found"}, status_code=404)


@app.put("/items/{item_id}")
async def update_item(item_id: int, first_name: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE new_table SET first_name = %s WHERE id = %s", (first_name, item_id)
    )
    connection.commit()
    connection.close()
    return JSONResponse(
        content={"message": "Item updated successfully"}, status_code=200
    )


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM new_table WHERE id = %s", (item_id,))
    connection.commit()
    connection.close()
    return JSONResponse(
        content={"message": "Item deleted successfully"}, status_code=200
    )
