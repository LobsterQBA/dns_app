FROM python:3.8-slim

# 复制 server.py 到容器中
COPY server.py /app/server.py

# 复制 DNS 记录文件
COPY dns_records.json /app/dns_records.json

# 设置工作目录为 /app
WORKDIR /app

# 运行权威服务器
CMD ["python", "server.py"]
