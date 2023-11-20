from fastapi import APIRouter
from loguru import logger

from models.demo1 import Demo
from utils.common import my_print

router = APIRouter(
    prefix="/normal",
    tags=["常规"],
)


@router.post("/test_normal", summary="普通函数")
@logger.catch
def text_review(demo: Demo):
    my_print("你好")
    return {"msg": demo.name}
