FROM python:3.8.15-bullseye
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN init=1 python /app/init_twnia_client.py

CMD ["/bin/sh", "/app/loop_main.sh", "&"]
