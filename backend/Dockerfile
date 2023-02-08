FROM python:3.7-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt update -y && apt upgrade -y && apt install netcat -y
RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . .

# CMD ["flask", "run"]
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8000", "app:app"]
