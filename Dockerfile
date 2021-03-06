FROM nvidia/cuda:11.0-devel-ubuntu18.04

# update packages
RUN apt-get -y update && apt-get install -y git wget ffmpeg make cmake python3-pip
RUN apt-get install -y build-essential

# install system dependencies
RUN apt-get install -y libatlas-base-dev libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev opencl-headers ocl-icd-opencl-dev libviennacl-dev libboost-dev libboost-all-dev
# libopencv-dev
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y libopencv-dev

# install python dependencies
RUN pip3 install pandas youtube-dl xcode pytube nvidia_ml_py3 torch

# working directory is /workspace
RUN mkdir workspace && cd workspace/

# get openpose cmake file:
RUN wget -q https://cmake.org/files/v3.13/cmake-3.13.0-Linux-x86_64.tar.gz
RUN tar xfz cmake-3.13.0-Linux-x86_64.tar.gz --strip-components=1 -C /usr/local

# install cuda drivers
RUN CUDNN_URL="http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/cudnn-8.0-linux-x64-v5.1.tgz"
# RUN CUDNN_RUL="https://developer.download.nvidia.com/compute/cuda/11.2.0/local_installers/cuda_11.2.0_460.27.04_linux.run"
RUN wget -c "http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/cudnn-8.0-linux-x64-v5.1.tgz"
RUN tar -xzf cudnn-8.0-linux-x64-v5.1.tgz -C /usr/local
RUN rm cudnn-8.0-linux-x64-v5.1.tgz || true && ldconfig

# clone openpose
RUN git_repo_url='https://github.com/CMU-Perceptual-Computing-Lab/openpose.git'
RUN git clone 'https://github.com/SandlerAlon/joint_extractor.git'
RUN cd joint_extractor && git clone --depth 1 'https://github.com/CMU-Perceptual-Computing-Lab/openpose.git'
# RUN sed -i 's/execute_process(COMMAND git checkout master WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/execute_process(COMMAND git checkout f019d0dfe86f49d1140961f8c7dec22130c83154 WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}\/3rdparty\/caffe)/g' openpose/CMakeLists.txt

# build openpose
# RUN cd openpose && rm -rf build || true && mkdir build && cd build && cmake .. && make -j`nproc` && cd ..

# copy current directory files:
COPY . /workspace

# Run app.py when the container launches without a command:
CMD ['ipython','app.py']
