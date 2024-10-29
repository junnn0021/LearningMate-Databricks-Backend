from fastapi import FastAPI, Depends, Response
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from app.db_connection import get_db_connection
from app.db.ai_movie_log import *
from app.db.ai_movie_request import *
from app.db.ai_movie_response import *
from app.db.ai_movie_response_review import *
from app.db.ai_movie_statics import *
from app.ai.ai_serve import *
from app.models import AiMovieRequest


# 환경변수 세팅 (.env 파일생성필요)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# set_env()
app = FastAPI()

# 전체 리스트 조회
@app.get("/test", response_model=list[AiMovieRequest])
def test() -> list[AiMovieRequest]:
    """
    쿼리 프로세스 설명
    1. QUERY(SELECT)
    2. MAKE ARRAY JSON DATA(Header + Rows)
    3. Make List of dict
    4. Validate & Convert Pydantic model from List(3)
    5. Return Pydantic model
        - default: return json data
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
def test01():
    return {"Hello": "Junseok World."}


@app.get("/translate")
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
    return ai_movie_request_call_procedure2("call2", "10.10.10.10", "")


# junseok MYSQL call procedure
@app.post("/movie/log/call")
async def save_ai_movie_log_call(log_data: AiMovieLog):
    return ai_movie_log_call_procedure(log_data)

@app.post("/movie/request/call3")
async def save_ai_movie_request_call(request_data: AiMovieRequest):
    return ai_movie_request_call_procedure3(request_data)

@app.post("/movie/response/call")
async def save_ai_movie_response_call(response_data: AiMovieResponse):
    return await ai_movie_response_call_procedure(response_data)

@app.post("/movie/review/call")
async def save_movie_review_call(review_data: AiMovieResponseReview):
    return ai_movie_review_call_procedure(review_data)

#AI server
@app.post("/ai")
async def ai_serve(request: Request):
    # request = "Recommend marvel movies with ratdings and director and plot. "
    data = await request.json()
    request_msg = data.get("request")
    print("request_msg : {0}". format(request_msg))
    completion_result = serve_completion(request_msg)
    print("AI 결과 : {0}". format(completion_result))
    if completion_result:
        return JSONResponse(content={"message": "Databricks 200", "result": completion_result})
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
