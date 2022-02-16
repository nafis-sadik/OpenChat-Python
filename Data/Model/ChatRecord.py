from typing import Optional

from pydantic.main import BaseModel


class ChatRecord(BaseModel):
    id: str
    sender: str
    message: Optional[str]
    receiver: str
