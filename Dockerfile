FROM python:latest

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
RUN cd /app && pip install -r requirements.txt
ENTRYPOINT ["python3", "cron.py"]
