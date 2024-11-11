from fastapi.responses import JSONResponse
from app.db_connection import get_db_connection
from typing import Any, Tuple
import socket

async def call_db_procedure(procedure_name: str, args: Tuple[Any, ...]) -> JSONResponse:
    try:
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.callproc(procedure_name, args)
                result = cursor.fetchall() 
            connection.commit()
            return JSONResponse(
                content={"code": 1, "message": "Request was successfully", "data": result}
            )
        except Exception as e:
            return JSONResponse(
                content={"code": 2, "error": str(e), "message": "An error occurred during the request"}
            )
        finally:
            connection.close()
    
    except (socket.error, ConnectionError) as e:
        return JSONResponse(
            content={"code": 2, "error": str(e), "message": "Network or server communication failed"},
            status_code=500 
        )
    except Exception as e:
        return JSONResponse(
            content={"code": 2, "error": str(e), "message": "An unexpected error occurred"},
            status_code=500
        )
