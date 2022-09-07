from fastapi import APIRouter

from Data.Model.UserModel import UserModel
from Service.Abstraction.IUserService import IUserService
from Service.Implementation.UserService import UserService

user_module = APIRouter(
    prefix='/api',
    tags=["Users"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)


@user_module.post('/signup')
async def register_user(user_model: UserModel):
    user_service: IUserService = UserService()
    return user_service.register_user(user_model)


@user_module.post('/login')
async def authenticate_user(username: str, password: str):
    user_service: IUserService = UserService()
    user_model: UserModel = UserModel()
    user_model.user_name = username
    user_model.password = password
    return user_service.authenticate_user(user_model)
