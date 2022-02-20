from typing import Optional

from pydantic.main import BaseModel


class ChatRecord(BaseModel):
    id: Optional[str]
    sender: Optional[str]
    message: Optional[str]
    receiver: Optional[str]
