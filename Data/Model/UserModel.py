import string
from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class UserModel(BaseModel):
    id: Optional[str]
    user_name: str
    email_id: Optional[str]
    password: str
    Gender: Optional[str]
    date_of_birth: Optional[datetime]
