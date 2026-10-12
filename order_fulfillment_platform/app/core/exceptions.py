from fastapi import Request
from fastapi.responses import JSONResponse

class DomainError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code, self.message, self.status_code = code, message, status_code

async def domain_exception_handler(request: Request, exc: DomainError):
    return JSONResponse(status_code=exc.status_code, content={'success': False, 'error': {'code': exc.code, 'message': exc.message}})
