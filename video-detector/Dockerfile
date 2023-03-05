FROM nvidia/cuda:11.7.0-devel-ubuntu22.04

ENV CUDA_HOME=/usr/local/cuda                                                          
ENV PATH=$PATH:/usr/local/cuda/bin

# Install base utilities
RUN apt update -y && apt upgrade -y && \
    apt install -y build-essential cmake && \
    apt install -y wget && \
    apt install -y git

# Install conda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda create --name detector python=3.7
SHELL ["conda", "run", "-n", "detector", "/bin/bash", "-c"]

# Install FFmpeg 4.4 with CUDA
## Compile and build
WORKDIR /opt
RUN git clone https://github.com/FFmpeg/FFmpeg.git
WORKDIR /opt/FFmpeg
RUN git checkout release/4.4
RUN ./configure --disable-x86asm --enable-shared --enable-avresample --prefix=/opt/ffmpeg/
RUN make -j 80 && make install

## Add env variables
ENV CPATH=$CPATH:/opt/ffmpeg/include
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/ffmpeg/lib
ENV CMAKE_PREFIX_PATH=$CMAKE_PREFIX_PATH:/opt/ffmpeg

# Install pip environment
WORKDIR /app/video-detector
COPY requirements.txt /app/video-detector
RUN python -m pip install --upgrade pip
RUN pip install numpy
RUN pip install -r requirements.txt

# Install OpenCV with CUDA
## Prepare necessary files
WORKDIR /opt/opencv
RUN git clone https://github.com/opencv/opencv_contrib.git
RUN git clone https://github.com/opencv/opencv.git
COPY install_opencv/ffmpeg-config.cmake /opt/ffmpeg

## Install opencv
ENV CXXFLAGS="-D__STDC_CONSTANT_MACROS"
WORKDIR /opt/opencv/opencv
RUN mkdir build
WORKDIR /opt/opencv/opencv/build
RUN cmake -D WITH_CUDA=ON \
    -D BUILD_TIFF=ON \
    -D BUILD_opencv_java=OFF \
    -D WITH_OPENGL=OFF \
    -D WITH_OPENCL=OFF \
    -D WITH_IPP=OFF \
    -D WITH_TBB=OFF \
    -D WITH_EIGEN=ON \
    -D WITH_V4L=OFF \
    -D WITH_VTK=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D CMAKE_BUILD_TYPE=RELEASE \
    -D BUILD_opencv_python2=OFF \
    -D CMAKE_INSTALL_PREFIX=~/.local/opencv \
    -D PYTHON3_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
    -D PYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D PYTHON3_EXECUTABLE=$(which python3) \
    -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
    -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv/opencv_contrib/modules \
    -D BUILD_EXAMPLES=OFF \
    -D ENABLE_CXX11=ON \
    -D WITH_FFMPEG=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D FFMPEG_DIR="/opt/ffmpeg/" \
    -D OPENCV_FFMPEG_SKIP_BUILD_CHECK=ON \
    -D OPENCV_FFMPEG_USE_FIND_PACKAGE=ON \
    -D BUILD_SHARED_LIBS=OFF \
    -D FFMPEG_DIR=/opt/ffmpeg/bin \
    ..
RUN make -j 80 && make install
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt

# Copy YoloV3
COPY detector/YOLOv3/ /app/video-detector/detector/YOLOv3/
WORKDIR /app/video-detector

# Download weights
WORKDIR detector/YOLOv3/weight/
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights
WORKDIR ../../../

# Copy the remaining files
COPY . /app/video-detector
WORKDIR /app/video-detector

# Compile YoloV3 after startup
# Compile nms during build wouldn't detect CUDA. Therefore,
# nms must be compiled after docker startup.
RUN echo "cd detector/YOLOv3/nms; sh build.sh; cd ../../../;" > init.sh

# Append initialization script
# RUN echo "python rpc_daemon.py" >> init.sh
# RUN echo "python traffic_terminal.py videos/minimal.mp4 --mode straight" >> init.sh
RUN echo "sleep 3600" >> init.sh

CMD ["conda", "run", "-n", "detector", "sh", "init.sh"]
