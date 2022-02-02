import string
from abc import ABC
from typing import Optional

from Data.Entities import Users
from Data.Model.UserModel import UserModel
from Service.Abstraction.IUserService import IUserService


class UserService(IUserService, ABC):
    def __init__(self):
        self.user_repository = None

    def register_user(self, user_model: UserModel) -> bool:
        try:
            user_entity: Users = Users()
            user_entity.user_name = user_model.user_name
            user_entity.Gender = user_model.Gender
            user_entity.date_of_birth = user_model.date_of_birth
            user_entity.email_id = user_model.email_id
            user_entity.id = self.user_repository.max(Users.id)
            self.user_repository.add(user_entity)
            return True
        except Exception as ex:
            print(str(ex))
            return False

    def authenticate_user(self, user_model: UserModel) -> [string]:
        try:
            user_entity: Users = self.user_repository.get(Users.user_name == user_model.user_name)
            if user_entity:
                return user_entity.password == user_model.password
            else:
                return ''
        except Exception as ex:
            print(str(ex))
            return ''