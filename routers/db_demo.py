from fastapi import APIRouter
from loguru import logger

from base.dababase import get_df_from_ck, get_df_from_mysql_pool, get_df_from_mysql_sqlalchemy
from models.demo1 import Demo
from utils.common import my_print

router = APIRouter(
    prefix="/db",
    tags=["数据库"],
)


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
    my_print(f"df_user:{df_user.shape}")
    my_print(f"df_user:{df_user}")
    return {"msg": demo.name}


@router.post("/test_mysql_create_pool", summary="aiomysql")
@logger.catch
async def test_ck(demo: Demo):
    """
    https://github.com/aio-libs/aiomysql
    :param demo:
    :return:
    """
    sql_content = "select * from api_article limit 1"
    my_print(f"sql_content:{sql_content}")
    data = await get_df_from_mysql_pool(sql_content)
    my_print(f"data1:{data}")
    return {"msg": "mysql create_pool"}


@router.post("/test_mysql_sqlalchemy", summary="aiomysql")
@logger.catch
async def test_ck(demo: Demo):
    """
    https://github.com/aio-libs/aiomysql \n
    不可用
    :param demo:
    :return:
    """
    sql_content = "select * from api_article limit 1"
    data = await get_df_from_mysql_sqlalchemy(sql_content)
    my_print(f"data2:{data}")
    return {"msg": "mysql sqlalchemy"}
