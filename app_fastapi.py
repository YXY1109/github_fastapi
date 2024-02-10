from contextlib import asynccontextmanager

# import redis #同步
import redis.asyncio as redis  # 异步
import uvicorn
from fastapi import FastAPI, applications
from fastapi.openapi.docs import get_swagger_ui_html
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from base.config import IS_DEBUG, RUN_HOST, RUN_PORT
from routers import db_demo, http_demo, normal_demo, redis_demo
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
    app_life.logger = logger

    print("redis连接")
    # https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html
    pool = redis.ConnectionPool.from_url("redis://@127.0.0.1:6379/0", max_connections=10,
                                         decode_responses=True)
    rc = redis.Redis.from_pool(pool)
    app_life.rc = rc
    yield
    # 第四步：清除日志记录器
    app_life.logger.remove()

    print("异步关闭redis连接")
    await rc.close()


app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 子路由
app.include_router(db_demo.router)
app.include_router(http_demo.router)
app.include_router(normal_demo.router)
app.include_router(redis_demo.router)

# 处理跨域
# 这里配置支持跨域访问的前端地址
origins = [
    "http://192.168.170.36",
    "http://192.168.170.36:8080",
    "http://192.168.180.239",
    "http://192.168.180.239:8088",
]

app.add_middleware(
    CORSMiddleware,
    # 这里配置允许跨域访问的前端地址
    allow_origins=origins,
    # 跨域请求是否支持 cookie， 如果这里配置true，则allow_origins不能配置*
    allow_credentials=True,
    # 支持跨域的请求类型，可以单独配置get、post等，也可以直接使用通配符*表示支持所有
    allow_methods=["*"],
    allow_headers=["*"],
)

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
