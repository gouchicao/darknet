FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04
LABEL maintainer="wang-junjian@qq.com"

RUN apt-get update && apt-get install -y \
    build-essential \
    nano \
    && rm -rf /var/lib/apt/lists/*

ADD ./darknet/ /darknet/

WORKDIR /darknet
RUN make && rm -rf obj

