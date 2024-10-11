# 基础镜像：使用Python 3.8轻量级版本
FROM python:3.8-slim

# 安装Flask和requests库
RUN pip install Flask requests

# 将本地的 server.py 文件复制到容器中的 /app 目录
COPY server.py /app/server.py

# 设置工作目录为 /app
WORKDIR /app

# 设置容器启动时执行的命令，运行用户服务器
CMD ["python", "server.py"]
