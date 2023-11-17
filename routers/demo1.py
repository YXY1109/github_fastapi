from fastapi import APIRouter
from loguru import logger

from base.dababase import get_df_from_ck
from models.demo1 import Demo
from utils.common import my_print

router = APIRouter(
    prefix="/demo",
    tags=["功能1"],
)


@router.post("/test_normal", summary="普通函数")
@logger.catch
def text_review(demo: Demo):
    my_print("你好")
    return {"msg": demo.name}


@router.post("/test_ck", summary="aioclickhouse")
@logger.catch
async def test_ck(demo: Demo):
    """
    接口详细信息 \n
    数据库依赖注入使用 \n
    :param demo: body参数 \n
    :param ck_client: ck数据库 \n
    :return:
    """
    sql_user = "SELECT DISTINCT tid,appid from ods_app_userbehivor_dist"
    df_user = await get_df_from_ck(sql_user, ["tid", "appid"])
    my_print(f"df_user:{df_user}")
    return {"msg": demo.name}


@router.post("/test_mysql", summary="aiomysql")
@logger.catch
async def test_ck(demo: Demo):
    pass


@router.post("/test_http", summary="aiohttp")
@logger.catch
async def test_ck(demo: Demo):
    pass
