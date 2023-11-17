# FASTAPI_基础框架

## 一，接口文档

```本地
本地：http://192.168.170.18:5000/docs
```

#### 配置git ssh

- 生成：ssh-keygen -t rsa -b 4096 -C "xxx.com"
- cd /root/.ssh/
- cat id_rsa.pub
- 在对应仓库配置公钥

#### conda环境

- 创建：conda create -n github_fastapi python=3.9
- cd /data/
- git clone git@xxx.git
- conda activate github_fastapi
- cd /github_fastapi
- pip install -r requirements.txt --use-pep517 -i https://pypi.tuna.tsinghua.edu.cn/simple

#### 服务器

- 获取最新代码

> conda activate github_fastapi && cd /data/github_fastapi && git pull

- 启动服务

> gunicorn app_fastapi:app -c gunicorn.py

- 查看进程

> pstree -ap|grep gunicorn

- 优雅的重启服务

> kill -HUP 30080

- 删除进程

> killall gunicorn

- 查看日志输出

> tail -f log/gunicorn_error.log
