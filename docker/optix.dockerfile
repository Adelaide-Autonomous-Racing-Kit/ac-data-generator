FROM nvcr.io/nvidia/pytorch:24.02-py3
ARG OPTIX_VERSION=8.0.0
ADD NVIDIA-OptiX-SDK-${OPTIX_VERSION}-linux64-x86_64 /usr/local/optix
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/optix/lib64

SHELL ["/bin/bash", "-c"] 
# Update and install system packages
RUN apt-get update && apt-get install build-essential \
    gfortran libopenblas-dev pkg-config ffmpeg libsm6 libxext6 git ninja-build -y
# Install intel embree v2.17.7
RUN wget https://github.com/embree/embree/releases/download/v2.17.7/embree-2.17.7.x86_64.linux.tar.gz \
    -O /tmp/embree.tar.gz -nv && \
    tar -xzf /tmp/embree.tar.gz --strip-components=1 -C /usr/local && \
    rm -rf /tmp/embree.tar.gz
ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib
# Install pyembree
RUN pip install numpy cython==0.29.36
RUN pip install https://github.com/scopatz/pyembree/releases/download/0.1.6/pyembree-0.1.6.tar.gz
# Install python packages
COPY requirements.txt .
RUN pip install -r requirements.txt
ENV OptiX_INSTALL_DIR=/usr/local/optix
RUN git clone https://github.com/lcp29/trimesh-ray-optix && cd trimesh-ray-optix && pip install .
# RUN pip install git+https://github.com/lcp29/trimesh-ray-optix
# Install ac-data-toolkit
COPY . .
RUN pip install -e .
# Run
ENV LANG=C.UTF-8
ENV CONFIG_PATH=monza.yaml
RUN apt-get install gdb -y
CMD gdb -ex r --args python3 test-optix.py