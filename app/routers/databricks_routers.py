from fastapi import APIRouter

router = APIRouter(
    prefix="/databricks",
)

@router.get("/question")
async def question():
    return {"msg:this is databricks question"}


@router.post("/question2")
async def question2():
    return {"msg:this is databricks question2"}


"""
아래 로직을 현재 라우터에 적용하면 됩니다.

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

"""