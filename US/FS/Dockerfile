FROM python:3.8-slim

# 安装 Flask
RUN pip install Flask

# 将 server.py 复制到容器中的 /app 目录
COPY server.py /app/server.py

# 设置工作目录为 /app
WORKDIR /app

# 运行斐波那契服务器
CMD ["python", "server.py"]
