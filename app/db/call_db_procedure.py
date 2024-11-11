from fastapi.responses import JSONResponse
from app.db_connection import get_db_connection
from typing import Any, Tuple

async def call_db_procedure(procedure_name: str, args: Tuple[Any, ...]) -> JSONResponse:
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.callproc(procedure_name, args)
            result = cursor.fetchall() 
        connection.commit()
        return JSONResponse(result, content={"message": "Request was successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        connection.close()