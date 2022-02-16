import glob
import os

from fastapi import APIRouter

from WebApplication.Controllers.ChatController import chat_service
from WebApplication.Controllers.UserController import user_module

router = APIRouter()
router.include_router(user_module)
router.include_router(chat_service)

__all__ = [os.path.basename(file_path)[:-3] for file_path in glob.glob(os.path.dirname(__file__) + "/*.py")]
