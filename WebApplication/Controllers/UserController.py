import os

import jwt
from fastapi import APIRouter

from Data.Model.UserModel import UserModel
from Service.Abstraction.IUserService import IUserService
from Service.Implementation.UserService import UserService
from fastapi.security import HTTPBearer

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

user_module = APIRouter(prefix='/api')


@user_module.post('/signup')
async def register_user(user_model: UserModel):
    user_service: IUserService = UserService()
    return user_service.register_user(user_model)


@user_module.post('/login')
async def authenticate_user(user_model: UserModel):
    user_name = user_model.user_name
    password = user_model.password
    user_service: IUserService = UserService()
    user_model: UserModel = UserModel()
    user_model.user_name = user_name
    user_model.password = password
    return user_service.authenticate_user(user_model)


@user_module.get('/get-friends/{token}')
async def get_friend_list(token: str):
    try:
        from dotenv import load_dotenv
        from pathlib import Path
        ROOT_DIR = str(Path(__file__).parent.parent.parent)
        if load_dotenv(dotenv_path=ROOT_DIR + '/.env'):
            secret_key = os.getenv('SECRET_KEY')
            security_algo = os.getenv("SECURITY_ALGORITHM")
            if secret_key is None or security_algo is None:
                return False
            from jwt.algorithms import get_default_algorithms
            print(get_default_algorithms())
            decoded = jwt.decode(token, secret_key, algorithms='HS256')
        return True
    except Exception as e:
        return str(e)
