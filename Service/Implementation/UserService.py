import os
import string
import uuid
from abc import ABC
from datetime import datetime, timedelta
from typing import Optional, Union, Any

import bcrypt
import jwt
from dotenv import load_dotenv

from Data.Entities import Users
from Data.Model.UserModel import UserModel
from Repositories.IRepositoryBase import IRepositoryBase
from Repositories.RepositoryBase import RepositoryBase
from Service.Abstraction.IUserService import IUserService
from Service.Implementation import ROOT_DIR


class UserService(IUserService, ABC):
    def __init__(self):
        self.user_repository: IRepositoryBase = RepositoryBase(Users)
        dotenv_path = ROOT_DIR + '/.env'
        load_dotenv(dotenv_path=dotenv_path)
        self.secret_key = os.getenv('SECRET_KEY')
        self.security_algo = os.getenv('SECURITY_ALGORITHM')

    def generate_token(self, username: Union[str, Any]):
        try:
            # Expired after 3 hours
            payload = {
                "exp": datetime.now() + timedelta(seconds=60 * 60 * 3), "username": username
            }
            encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.security_algo)
            return encoded_jwt
        except Exception as ex:
            return str(ex)

    def register_user(self, user_model: UserModel) -> Optional[bool]:
        try:
            users_found: list = self.user_repository.get(Users.user_name == user_model.user_name)
            if users_found is None or len(users_found) > 0:
                return False
            user_entity: Users = Users()
            user_entity.password = bcrypt.hashpw(bytes(user_model.password, 'utf-8'), bcrypt.gensalt())
            user_entity.user_name = user_model.user_name
            user_entity.Gender = user_model.Gender
            user_entity.date_of_birth = user_model.date_of_birth
            user_entity.email_id = user_model.email_id
            user_entity.id = uuid.uuid4().__str__()
            self.user_repository.add(user_entity)
            return True
        except Exception as ex:
            print(str(ex))
            return None

    def authenticate_user(self, user_model: UserModel) -> Optional[str]:
        try:
            user_entity: list = self.user_repository.get(Users.user_name == user_model.user_name)
            if user_entity is not None and len(user_entity) > 0:
                if bcrypt.checkpw(user_model.password.encode('utf-8'), user_entity[0].password):
                    return self.generate_token(username=user_model.user_name)
                else:
                    return 'Wrong Password'
            else:
                return 'User not found'
        except Exception as ex:
            print(str(ex))
            return None

    def get_username_from_user_id(self, user_id: string) -> str:
        user = self.user_repository.get(Users.id == user_id)
        if user is not None and len(user) > 0:
            return user[0].user_name
        return ''
