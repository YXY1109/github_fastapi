from datetime import datetime, timedelta
import time

from loguru import logger
from orjson import orjson
from pydantic import typing
from starlette.responses import JSONResponse


class ORJSONResponse(JSONResponse):
    """
    解决fastapi：ValueError: Out of range float values are not JSON compliant
    """
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return orjson.dumps(content)


def my_print(message):
    logger.info(message)
    print(message)
    print("~" * 50)


def timer(func):
    """
    装饰器，函数执行的时间计时器
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('共耗时约 {:.2f} 秒'.format(time.time() - start))
        return res

    return wrapper


def get_today_time(day=0, is_zero=False):
    """
    获取今天的时间
    """
    today = datetime.today() - timedelta(days=day)
    if is_zero:
        time_format = '%Y-%m-%d 00:00:00'
    else:
        time_format = '%Y-%m-%d %H:%M:%S'
    today_time = today.strftime(time_format)
    return today_time


if __name__ == '__main__':
    print(get_today_time())
