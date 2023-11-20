import aiomysql
import pandas as pd
from aiochclient import ChClient
from aiohttp import ClientSession
from aiomysql.sa import create_engine

from base import mysql_user, mysql_db, mysql_host, mysql_password, mysql_port
from utils.config import global_config


async def get_df_from_ck(ck_sql, columns):
    """
    https://github.com/maximdanilchenko/aiochclient

    :return:
    """
    async with ClientSession() as session:
        ck_host = global_config.get('CK', 'HOST')
        ck_url = f'http://{ck_host}:8123'
        ck_user = global_config.get('CK', 'USER')
        ck_password = global_config.get('CK', 'PASSWORD')
        ck_database = global_config.get('CK', 'DB')
        ck_client = ChClient(session, url=ck_url, user=ck_user, password=ck_password,
                             database=ck_database)
        data_result = await ck_client.fetch(ck_sql)
        df_data = pd.DataFrame(data_result, columns=columns)
        print(f"df_data:{df_data}")
        return df_data


async def get_df_from_mysql_sqlalchemy(mysql_sql):
    """
    https://github.com/aio-libs/aiomysql/discussions/908
    不可用，还需要修改代码，比较麻烦
    :param mysql_sql:
    :return:
    """

    engine = await create_engine(user=mysql_user, db=mysql_db, host=mysql_host, password=mysql_password,
                                 port=int(mysql_port))
    async with engine.acquire() as conn:
        mysql_result = await conn.execute(mysql_sql)
        print(f"mysql_result,id:{mysql_result.id}")
        print(f"mysql_result,val:{mysql_result.val}")
        return mysql_result

    # engine.close()
    # await engine.wait_closed()


async def get_df_from_mysql_pool(mysql_sql):
    pool = await aiomysql.create_pool(host=mysql_host, port=int(mysql_port),
                                      user=mysql_user, password=mysql_password,
                                      db=mysql_db)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(mysql_sql)
            print(cur.description)
            r = await cur.fetchone()
            print(f"r:{r}")
            return r

    # pool.close()
    # await pool.wait_closed()


async def get_mysql_pool():
    pool = await aiomysql.create_pool(host=mysql_host, port=int(mysql_port),
                                      user=mysql_user, password=mysql_password,
                                      db=mysql_db)
    try:
        print(111)
        yield pool
    finally:
        print(222)
        pool.close()
        await pool.wait_closed()
