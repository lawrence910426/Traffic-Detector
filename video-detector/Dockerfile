# FROM nvidia/cuda:11.7.0-devel-ubuntu22.04
FROM nvcr.io/nvidia/pytorch:23.03-py3

ENV CUDA_HOME=/usr/local/cuda                                                          
ENV PATH=$PATH:/usr/local/cuda/bin

# Setup timezone
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install base utilities
RUN apt update -y && apt upgrade -y && \
    apt install -y build-essential cmake && \
    apt install -y wget && \
    apt install -y git && \
    apt install -y libx264-dev && \
    apt install -y python3-tk

# Install Intel oneAPI
RUN curl -fsSL https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS-2023.PUB | apt-key add -
RUN echo "deb [trusted=yes] https://apt.repos.intel.com/oneapi all main " > /etc/apt/sources.list.d/oneAPI.list
RUN apt update -y && apt upgrade -y && apt install intel-basekit-getting-started intel-oneapi-advisor intel-oneapi-ccl-devel intel-oneapi-common-licensing intel-oneapi-common-vars intel-oneapi-dev-utilities intel-oneapi-ipp-devel intel-oneapi-tbb-devel -y

ENV CPATH=$CPATH:/opt/intel/oneapi/ipp/latest/include:/opt/intel/oneapi/tbb/latest/include/tbb
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/intel/oneapi/ipp/latest/lib/intel64:/opt/intel/oneapi/tbb/latest/lib/intel64/gcc4.8
ENV LIBRARY_PATH=$LIBRARY_PATH:/opt/intel/oneapi/ipp/latest/lib/intel64:/opt/intel/oneapi/tbb/latest/lib/intel64/gcc4.8

# Install conda
# ENV CONDA_DIR /opt/conda
# RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && /bin/bash ~/miniconda.sh -b -p /opt/conda
# ENV PATH=$CONDA_DIR/bin:$PATH
# RUN conda create --name detector python=3.7
# SHELL ["conda", "run", "-n", "detector", "/bin/bash", "-c"]

# Install FFmpeg 4.4 with CUDA
## Compile and build
WORKDIR /opt
RUN git clone https://github.com/FFmpeg/FFmpeg.git
WORKDIR /opt/FFmpeg
RUN git checkout release/4.4
RUN ./configure --disable-x86asm --enable-shared --enable-gpl \
    --enable-libx264 --enable-avresample --prefix=/opt/ffmpeg/
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
    -D WITH_IPP=ON \
    -D WITH_TBB=ON \
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

# Remove NGC's opencv
RUN pip uninstall -y opencv

# Create YoloV3 weight placeholder
COPY detector/YOLOv3/weight/ /app/video-detector/detector/YOLOv3/weight/
WORKDIR /app/video-detector

# Download weights
WORKDIR detector/YOLOv3/weight/
RUN wget https://pjreddie.com/media/files/yolov3.weights
RUN wget https://pjreddie.com/media/files/yolov3-tiny.weights

# Download ReID model
COPY tracker/deep_sort/deep/checkpoint /app/video-detector/tracker/deep_sort/deep/checkpoint
WORKDIR /app/video-detector/tracker/deep_sort/deep/checkpoint
RUN wget https://github.com/JDAI-CV/fast-reid/releases/download/v0.1.1/veriwild_bot_R50-ibn.pth

# Install ReID
COPY thirdparty /app/video-detector/thirdparty
WORKDIR /app/video-detector/thirdparty/fast-reid/docs
RUN pip install -r requirements
RUN pip install tensorboard==2.13.0 --force-reinstall
WORKDIR /app/video-detector/thirdparty/fast-reid/fastreid/evaluation/rank_cylib
RUN make all

# Fix symbolic link (Ubuntu 22.04 bug)
# RUN rm /opt/conda/envs/detector/lib/libstdc++.so*
# RUN ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /opt/conda/envs/detector/lib/libstdc++.so.6
# RUN ln -s /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /opt/conda/envs/detector/lib/libstdc++.so

# Copy the remaining files
COPY . /app/video-detector
WORKDIR /app/video-detector

# Compile YoloV3 after startup
# Compile nms during build wouldn't detect CUDA. Therefore,
# nms must be compiled after docker startup.
RUN echo "cd detector/YOLOv3/nms; sh build.sh; cd ../../../;" > init.sh

# Append initialization script
# RUN echo "python rpc_daemon.py" >> init.sh
RUN echo "python traffic_terminal.py videos/minimal.mp4 --mode straight --fastreid" >> init.sh
# RUN echo "sleep 86400" >> init.sh

CMD [ "sh", "init.sh" ]
# CMD ["conda", "run", "-n", "detector", "sh", "init.sh"]
