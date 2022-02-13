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


# @user_module.get('/get-friends', dependencies=[Depends(reusable_oauth2)])
# async del get_friend_list():