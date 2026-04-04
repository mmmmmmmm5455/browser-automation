# Dockerfile - 用于 Docker �署
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
PLAYWRIGHT_BROWS=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node.js（Playwright 需要）
RUN wget -qO- https://deb.nodesource.com/setup_18.x | bash \
    && apt-get install -y nodejs \
    && rm -f node-setup_18.x \
    && node --version

# 安装 Playwright 浏览器依赖
RUN npx playwright install --with-deps chromium

# 复制项目文件
COPY . /app

# 安装 Python 依赖
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# 创建必要的目录
RUN mkdir -p /app/screenshots /app/data /app/logs

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["python", "-m", "app.main:app"]
