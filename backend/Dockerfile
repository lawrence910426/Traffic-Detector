FROM nvidia/cuda:11.7.0-devel-ubuntu22.04

WORKDIR /usr/src/app

RUN apt update -y && \
    apt upgrade -y && \
    apt install tmux vim wget build-essential cmake git -y && \
    apt install -y libx264-dev

# Install conda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda create --name backend python=3.7
SHELL ["conda", "run", "-n", "backend", "/bin/bash", "-c"]

# Install FFmpeg 4.4 with GPU support
WORKDIR /opt
RUN git clone https://github.com/FFmpeg/FFmpeg.git
WORKDIR /opt/FFmpeg
RUN git checkout release/4.4
RUN ./configure --disable-x86asm --enable-shared --enable-gpl \
    --enable-libx264 --enable-avresample --prefix=/opt/ffmpeg/
RUN make -j 80
RUN make install

# Add env vars for ffmpeg
ENV PATH=$PATH:/opt/ffmpeg/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/ffmpeg/lib

# Install other dependencies
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the remain files
COPY . .
EXPOSE 8000

# Test flask running
# CMD ["flask", "run"]

# Only 1 worker is allowed.
# CMD [ "sleep", "86400" ]
CMD [ \
    "rm", "-rf", "/mnt/video-in", "&&", "rm", "-rf", "/mnt/video-out", "&&", \
    "conda", "run", "-n", "backend", \
    "gunicorn", "-t", "86400", "-w", "1", "--bind", "0.0.0.0:8000", "app:app" \
]


# Run with rpc terminal
# CMD ["conda", "run", "-n", "backend", "python", "rpc_terminal.py", "minimal.mp4"]
