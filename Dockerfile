# 使用 Python 3.9 作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制当前目录下的文件到工作目录
COPY . /app

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露容器端口
EXPOSE 5000

# 设置环境变量
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# 运行 Flask 应用程序
CMD ["flask", "run", "--host=0.0.0.0"]