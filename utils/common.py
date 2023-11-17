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


if __name__ == '__main__':
    pass
