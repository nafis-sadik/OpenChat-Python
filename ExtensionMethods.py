import os
import jwt
from fastapi import Request


async def get_current_user(request: Request):
    secret_key: str = os.getenv('SECRET_KEY')
    security_algo: str = os.getenv("SECURITY_ALGORITHM")
    token = request.headers.get('Authorization').split()[1].replace('"', '')
    decoded: dict = jwt.decode(jwt=token, key=secret_key, algorithms=security_algo)
    print(decoded['username'])