FROM python:3.7-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . .

# CMD ["flask", "run"]
CMD ["gunicorn", "-w", "4", "app:app"]