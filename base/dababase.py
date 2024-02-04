import aiomysql
import pandas as pd
from aiochclient import ChClient
from aiohttp import ClientSession
from aiomysql.sa import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from base import mysql_user, mysql_db, mysql_host, mysql_password, mysql_port
from utils.config import global_config

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"
# 输出执行的SQL语句
SQLALCHEMY_ECHO = False


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


def get_engine():
    my_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=SQLALCHEMY_ECHO, pool_size=20,
                              pool_recycle=60, pool_pre_ping=True, max_overflow=10)
    return my_engine


def get_session_1():
    """
    方式一，需要自己维护关闭
    :return:
    """
    session = sessionmaker(bind=get_engine())
    # 线程安全
    my_session = scoped_session(session)
    return my_session


def get_session_2():
    """
    方式二，不需要维护
    :return:
    """
    session = sessionmaker(bind=get_engine())
    # 线程安全
    my_session = scoped_session(session)

    # https://copyprogramming.com/howto/how-to-correctly-use-sqlalchemy-within-fastapi-or-arq-for-mysql
    # https://www.cnblogs.com/ChangAn223/p/11277468.html
    # https://sunnyingit.github.io/book/section_python/SQLalchemy-engine.html
    try:
        yield my_session
    finally:
        print("主动关闭session")
        my_session.close()
    # 方式二使用：get_session().__next__()
