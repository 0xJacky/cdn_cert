FROM python:latest

WORKDIR /app
COPY ./requirements.txt ./requirements.txt
COPY ./cdncert.py ./cdncert.py
COPY ./config-template.ini ./config-template.ini
COPY ./core.py ./core.py
COPY ./cron.py ./cron.py
COPY ./database.py ./database.py
COPY ./logger.py ./logger.py
COPY ./mail.py ./mail.py
COPY ./settings.py ./settings.py

RUN cd /app && pip install -r requirements.txt
ENTRYPOINT ["python3", "cron.py"]
