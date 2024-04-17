import time
from datetime import timedelta

from fastapi import Request
from fastapi.logger import logger as fastapi_logger
from fastapi.security import OAuth2PasswordBearer
from jwt import decode
from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.auth import create_access_token
from src.utils.const import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class StructlogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.start_time = time.time()
        response = await call_next(request)

        structlog_message = {
            "remote_addr": request.client.host,
            "remote_port": request.client.port,
            "request_method": request.method,
            "request_path": request.url.path,
            "status_code": response.status_code,
            "response_time": (time.time() - request.state.start_time) * 1000,
        }

        fastapi_logger.info("Request completed", structlog_message)

        return response


class TokenRefreshMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        excluded_paths = ("/docs", "/openapi.json", "/register", "/login")
        if request.url.path.endswith(excluded_paths):
            return await call_next(request)
        if '/' == request.url.path:
            return await call_next(request)
        # try:
        token = await oauth2_scheme(request)
        user_id = decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
        response = await call_next(request)
        if user_id:
            access_token = create_access_token(
                data={"sub": str(user_id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            response.headers["Authorization"] = f"Bearer {access_token}"
        return response
        # except Exception:
        #     print('нет токена')
