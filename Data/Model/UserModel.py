from datetime import datetime
from typing import Optional

from pydantic.fields import Field
from pydantic.main import BaseModel


class UserModel(BaseModel):
    id: Optional[str]
    user_name: str = Field(None, title='', max_length=300)
    email_id: Optional[str]
    password: str = Field(None, title='', max_length=300)
    Gender: Optional[str]
    date_of_birth: Optional[datetime]
