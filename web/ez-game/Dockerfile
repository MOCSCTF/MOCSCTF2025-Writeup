# 基于官方 flask 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 拷贝项目文件
COPY src/app.py .
COPY src/templates/ ./templates/

# 拷贝 flag.txt 到根目录
COPY flag.txt /flag.txt

# 安装 Flask 和 python_jwt
RUN pip install --no-cache-dir flask python_jwt==3.3.3

# 设置环境变量（可选）
ENV FLASK_APP=app.py

# 容器启动时运行 Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=9999"]

EXPOSE 9999
