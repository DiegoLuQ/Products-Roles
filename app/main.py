from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from core.api.base import router
from fastapi.exceptions import RequestValidationError
from core.config.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import pytz
import datetime
from ratelimit import limits, RateLimitException 

chile_tz = pytz.timezone("America/Santiago")


class RequestInfoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method in ["GET", "POST", "PATCH", "DELETE"]:

            ip = request.client.host
            url_pth = request.url.path
            current_time = datetime.datetime.now(chile_tz)
            response = await call_next(request)
            
            log = f"{request.method} {response.status_code} request received from IP {ip} URL {url_pth} at {current_time}"
            data = { f"{current_time.strftime('%Y%m%d%H%M%S%f')}": {
                    "method":request.method,
                    "status_code": response.status_code,
                    "ip_user":ip,
                    "path":url_pth,
                    "date":f"{current_time}"}}
            print(log)
            # with open(settings.LOGS, 'a', encoding="utf-8") as archivo:
            #     archivo.write( str(data) + ',' + "\n")

        return response

middleware = [
    Middleware(RequestInfoMiddleware),
]

def start_app():
    app = FastAPI(title=settings.TITLE, contact=settings.CONTACT, version=settings.VERSION, description=settings.DESCRIPTION, middleware=middleware)
    app.include_router(router)
    return app

app = start_app()

@app.exception_handler(RateLimitException)
async def rate_limit_exception_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"msg": "too many requests, please try again later."},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422, content={"detail":"the data sent is not valid"}
    )

@app.get("/")
def home():
    return {"URL":settings.URL_WEB}


