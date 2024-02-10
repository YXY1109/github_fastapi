import time

from loguru import logger
from orjson import orjson
from pydantic import typing
from pypinyin import lazy_pinyin
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


def chinese_to_pinyin(chine_str):
    """
    中文转拼音
    :param chine_str:
    :return:
    """
    result = "_".join(lazy_pinyin(chine_str))
    return result


if __name__ == '__main__':
    pass
