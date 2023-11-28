# 使用 Python 基础镜像并安装 Poetry
FROM python:3.10-slim
RUN python3 -m pip install poetry && poetry config virtualenvs.create false

# 设置工作目录
WORKDIR /app

# 将项目的依赖项文件复制到 Docker 镜像中
COPY pyproject.toml poetry.lock* ./

# 安装项目的依赖项
RUN poetry install --no-root --no-dev

# 将项目的源代码复制到 Docker 镜像中
COPY . .

# 暴露 Django 运行所需的端口
EXPOSE 8000

# 设置 Docker 镜像的默认命令
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
