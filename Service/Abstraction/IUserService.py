import string
from typing import Optional

from Data.Model.UserModel import UserModel


class IUserService:
    def register_user(self, user_model: UserModel) -> [bool]:
        raise NotImplementedError

    def authenticate_user(self, user_model: UserModel) -> [string]:
        raise NotImplementedError
