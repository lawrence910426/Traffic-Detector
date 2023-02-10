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
WORKDIR /app/video-detector
COPY requirements.txt /app/video-detector
RUN python -m pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements.txt

# Install OpenCV by conda
RUN conda install -c conda-forge opencv 

# Copy YoloV3
COPY detector/YOLOv3/ /app/video-detector/detector/YOLOv3/
WORKDIR /app/video-detector

# Download weights
WORKDIR detector/YOLOv3/weight/
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights
WORKDIR ../../../

# Compile YoloV3
WORKDIR detector/YOLOv3/nms
RUN sh build.sh
WORKDIR ../../../

# Copy the remaining files
COPY . /app/video-detector

# Build the gRPC proto
WORKDIR /app/video-detector/rpc_server
RUN bash generate_proto.sh

WORKDIR /app/video-detector

# CMD ["conda", "run", "-n", "detector", "python", "rpc_server/daemon.py"]
CMD ["conda", "run", "-n", "detector", "python", "traffic_terminal.py", "videos/10sec.mp4", "--mode", "straight"]
