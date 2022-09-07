import string
from typing import Optional

from Data.Model.UserModel import UserModel


class IUserService:
    def register_user(self, user_model: UserModel) -> Optional[bool]:
        raise NotImplementedError

    def authenticate_user(self, user_model: UserModel) -> Optional[str]:
        raise NotImplementedError

    def get_username_from_user_id(self, user_id: string) -> str:
        raise NotImplementedError
