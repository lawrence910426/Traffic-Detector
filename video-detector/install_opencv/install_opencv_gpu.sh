# Dependencies. Recommend python 3.7
# 1) nvidia/cuda/11.0   
# 2) intel-oneapi-compilers-classic-2021.7.0-gcc-9.4.0-zonkhnf   
# 3) gcc-7.5.0-gcc-9.4.0-hycwc7d 
# 4) pkg-config-0.29.1-gcc-9.4.0-pcskm2i

# Install FFmpeg 4.4
git clone git@github.com:FFmpeg/FFmpeg.git
cd FFmpeg
git checkout release/4.4
./configure --enable-shared --enable-avresample --prefix=/home/lawrence910427/.local/ffmpeg/
make -j 80
make install

# Install OpenCV with CUDA
cp ffmpeg-config.cmake /home/lawrence910427/.local/ffmpeg/ffmpeg-config.cmake
export CXXFLAGS="-D__STDC_CONSTANT_MACROS"
cmake -D WITH_CUDA=ON \
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
    -D OPENCV_EXTRA_MODULES_PATH=/home/lawrence910427/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=OFF \
    -D ENABLE_CXX11=ON \
    -D WITH_FFMPEG=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D FFMPEG_DIR="/home/lawrence910427/.local/ffmpeg" \
    -D OPENCV_FFMPEG_SKIP_BUILD_CHECK=ON \
    -D OPENCV_FFMPEG_USE_FIND_PACKAGE=ON \
    -D BUILD_SHARED_LIBS=OFF \
    ..
make -j 80
make install

# Add LD_LIBRARY_PATH (to .bash_profile)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/lawrence910427/.local/