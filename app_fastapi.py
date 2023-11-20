from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from loguru import logger
from starlette.staticfiles import StaticFiles

from base.config import IS_DEBUG, RUN_HOST, RUN_PORT
from routers import db_demo, http_demo, normal_demo
from utils.common import ORJSONResponse


# 使用本地静态文件
def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url='./static/swagger-ui-bundle.js',
        swagger_css_url='./static/swagger-ui.css'
    )


applications.get_swagger_ui_html = swagger_monkey_patch

# 第一步：创建一个日志记录器
# 清除默认日志记录器
logger.remove()
# 创建新的日志记录器
# 每天生成一个日志文件，文件名称时年-月-日的形式命名
# 日志文件保存7天
logger.add(
    sink="./log/{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="1 days",
    retention="10 days"
)


@asynccontextmanager
async def lifespan(app_life: FastAPI):
    # 第二步：为app注册一个公共的日志记录器
    app_life.state.logger = logger
    yield
    # 第四步：清除日志记录器
    app_life.state.logger.remove()


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 子路由
app.include_router(db_demo.router)
app.include_router(http_demo.router)
app.include_router(normal_demo.router)

if __name__ == '__main__':
    if IS_DEBUG:
        print("开始启动本地服务：")
        uvicorn.run(app="app_fastapi:app", host=RUN_HOST, port=RUN_PORT, reload=IS_DEBUG)
    else:
        print("服务器使用命令行启动")
        # 正式使用，后台服务
        # gunicorn app_fastapi:app -c gunicorn.py
        # 调试使用，前台服务
        # uvicorn.run(app="app_fastapi:app", host=RUN_HOST, port=RUN_PORT, reload=IS_DEBUG)
