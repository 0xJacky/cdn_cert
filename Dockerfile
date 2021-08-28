FROM python:latest

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN cd /app && pip install -r requirements.txt
ENTRYPOINT ["python3", "cron.py"]
