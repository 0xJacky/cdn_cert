FROM python:latest
VOLUME ['/app', '/cert']
WORKDIR /app
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
COPY ./sources.list /etc/apt/sources.list
RUN apt update -y && apt install cron -y
