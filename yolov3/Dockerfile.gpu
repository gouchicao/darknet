FROM nvidia/cuda:10.0-cudnn7-devel-ubuntu18.04
LABEL maintainer="wang-junjian@qq.com"

RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-pip \
    nano \
    && rm -rf /var/lib/apt/lists/*

ADD ./darknet/ /darknet/
ADD *.py /darknet/

WORKDIR /darknet
RUN make GPU=1 CUDNN=1 && rm -rf obj

