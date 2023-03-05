FROM python:3.7-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt update -y && apt upgrade -y && apt install netcat -y
RUN pip3 install -r requirements.txt

# Install ffmpeg (w/o GPU support)
RUN apt install ffmpeg -y

EXPOSE 8000

COPY . .

# Test flask running
# CMD ["flask", "run"]

# Only 1 worker is allowed.
CMD ["gunicorn", "-t", "3600", "-w", "1", "--bind", "0.0.0.0:8000", "app:app"]

# Run with rpc terminal
# CMD ["python", "rpc_terminal.py", "minimal.mp4"]
