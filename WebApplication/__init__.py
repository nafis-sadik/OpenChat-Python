import os
import string
import time
from datetime import datetime
from pathlib import Path

import jwt
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette import responses

# Create the app
from WebApplication.Controllers import router

app = FastAPI(
    title='Open Chat',
    version='1.0.0'
)

# Add origins in this array to allow them only
origins = [
    "http://localhost",
    "http://localhost:4200",
]

# Add middlewares, origin also comes as middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount specific folders
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable routing
app.include_router(router)

public_routs = [
    '/api/signup',
    '/api/login',
    '/docs',
    '/redoc',
    '/openapi.json',
    '/favicon.ico',
    '/senders'
]


@app.middleware("http")
async def validate_jwt(request: Request, call_next):
    try:
        start_time = time.time()
        application_root_path = str(Path(__file__).parent.parent)
        if load_dotenv(dotenv_path=application_root_path + '/.env'):
            secret_key: string = os.getenv('SECRET_KEY')
            security_algo: string = os.getenv("SECURITY_ALGORITHM")
            if secret_key is None or security_algo is None:
                raise HTTPException(
                    status_code=401,
                    detail='Unable to parse authentication token'
                )
            token: string = request.headers.get('bearer')
            current_route: string = request.url.path

            # No auth required if it's public url
            if current_route in public_routs:
                response = await call_next(request)
                process_time = time.time() - start_time
                response.headers["X-Process-Time"] = str(process_time)
                return response
            else:
                if token:
                    decoded: dict = jwt.decode(token, secret_key, algorithms=security_algo)
                    if datetime.fromtimestamp(decoded['exp']) >= datetime.now() or current_route in public_routs:
                        response = await call_next(request)
                        process_time = time.time() - start_time
                        response.headers["X-Process-Time"] = str(process_time)
                        return response
                else:
                    return responses.JSONResponse(
                        status_code=401,
                        content='Unauthorized Access'
                    )
        return responses.JSONResponse(
            status_code=401,
            content='Unauthorized Access'
        )
    except Exception as e:
        return responses.JSONResponse(
            status_code=401,
            content=str(e)
        )


# @app.middleware('ws')
# async def validate_jwt_for_socket(request: Request, call_next):
#     print(request)
#     print(call_next)
#     return
