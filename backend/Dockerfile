FROM python:3.7-buster
ARG LOCAL_IP


WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt install netcat
RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . .

# CMD ["flask", "run"]
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8000", "app:app"]
