from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel


class ChatGroup(BaseModel):
    id: Optional[str]
    group_name: Optional[str]
    group_create_date: Optional[datetime]
    group_founder: Optional[str]
    password: Optional[str]
