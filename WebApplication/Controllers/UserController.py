from fastapi import APIRouter
from fastapi.security import HTTPBearer

from Data.Model.UserModel import UserModel
from Service.Abstraction.IUserService import IUserService
from Service.Implementation.UserService import UserService

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
    user_service: IUserService = UserService()
    return user_service.authenticate_user(user_model)
