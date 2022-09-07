from datetime import datetime
from typing import Optional

from pydantic.fields import Field
from pydantic.main import BaseModel


class UserModel(BaseModel):
    id: Optional[str]
    user_name: str = Field(None, title='UserName', max_length=100)
    email_id: Optional[str] = Field(None, title='Email Address', max_length=100)
    phone_number: int = Field(None, title='Phone Number')
    password: str = Field(None, title='Password', max_length=18)
    Gender: Optional[str] = Field(None, title='Gender', max_length=10)
    date_of_birth: Optional[datetime] = Field(None, title='Date of birth (UTC Time)')
