import time

import aiohttp
import httpx
import requests
from fastapi import APIRouter
from loguru import logger

from base.dababase import get_df_from_ck, get_df_from_mysql_pool, get_df_from_mysql_sqlalchemy
from models.demo1 import Demo
from utils.common import my_print

router = APIRouter(
    prefix="/http",
    tags=["网络请求"],
)


@router.post("/test_requests", summary="requests")
@logger.catch
async def test_ck(demo: Demo):
    """
    https://github.com/aio-libs/aiohttp
    :param demo:
    :return:
    """
    response = requests.get("https://baidu.com")
    print(response.status_code)
    return {"msg": f"requests的请求"}


@router.post("/test_aiohttp", summary="aiohttp")
@logger.catch
async def test_ck(demo: Demo):
    """
    https://github.com/aio-libs/aiohttp
    :param demo:
    :return:
    """

    async with aiohttp.ClientSession() as session:
        async with session.get("https://baidu.com") as response:
            print(response.status)

    return {"msg": f"aiohttp的请求"}


@router.post("/test_httpx", summary="httpx")
@logger.catch
async def test_ck(demo: Demo):
    """
    https://github.com/projectdiscovery/httpx
    :param demo:
    :return:
    """
    async with httpx.AsyncClient() as client:
        response = await client.get("https://baidu.com")
        print(response.status_code)
    return {"msg": f"httpx的请求"}
