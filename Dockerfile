FROM ubuntu:18.04

LABEL MAINTAINER="epassaro"

ARG BASE_NAME=lpt-ubuntu-${VERSION}

RUN apt-get update && \
    apt-get install -y build-essential libjpeg62 \
    liblapack3 libceres1 jhead python3 python3-pil \
    python3-ruamel.yaml \
    rsync wget && \
    apt-get clean
    
WORKDIR /opt

RUN wget -q https://github.com/epassaro/linux-photogrammetry-tools/releases/download/latest/${BASE_NAME}.tar.gz  && \
    tar zxf ${BASE_NAME}.tar.gz && \
    rm -f ${BASE_NAME}.tar.gz

WORKDIR /opt/${BASE_NAME}

CMD ["/bin/bash"]
