from fastapi import APIRouter

from Data.Model.UserModel import UserModel
from Service.Abstraction.IUserService import IUserService
from Service.Implementation.UserService import UserService

user_module = APIRouter(prefix='/api')


@user_module.post('/signup')
async def register_user(user_model: UserModel):
    user_service: IUserService = UserService()
    return user_service.register_user(user_model)


@user_module.get('/login/{user_name}/{password}')
async def authenticate_user(user_name: str, password: str):
    user_service: IUserService = UserService()
    user_model: UserModel = UserModel()
    user_model.user_name = user_name
    user_model.password = password
    return user_service.authenticate_user(user_model)
