from fastapi import APIRouter
from loguru import logger
from models.demo1 import Demo
from utils.common import my_print

router = APIRouter(
    prefix="/demo",
    tags=["功能1"],
)


@router.post("/test", summary="hello word")
@logger.catch
def text_review(demo: Demo):
    my_print("你好")
    return {"msg": demo.name}
