import pandas as pd
from aiochclient import ChClient
from aiohttp import ClientSession

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
