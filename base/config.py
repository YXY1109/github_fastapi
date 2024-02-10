import os

# 项目根目录
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# /Users/cj/PycharmProjects/github_fastapi
print(f"BASE_PATH:{BASE_PATH}")

IS_DEBUG = True

if IS_DEBUG:
    RUN_HOST = "192.168.170.18"
    RUN_PORT = 5001
else:
    RUN_HOST = "xxx.xxx.xxx.xxx"
    RUN_PORT = 5002

"""
Milvus相关
"""
CLIP_DOWNLOAD_PATH = os.path.join(BASE_PATH, "static/models/")
