from fastapi import APIRouter, Request
from loguru import logger

from models.demo1 import Demo
from utils.common import my_print

router = APIRouter(
    prefix="/redis",
    tags=["redis"],
)


@router.get("/test_redis")
async def test_redis(request: Request):
    """
    测试redis的连接使用
    """
    await request.app.rc.set("full_name", "john doe1")
    full_name = await request.app.rc.get("full_name")
    return {"code": 200, "msg": f"测试redis的连接使用:{full_name}"}
