FROM alicevision/popsift:version-0.9-cuda10.2-ubuntu18.04

LABEL MAINTAINER="epassaro"

ARG VERSION
ARG BASENAME=lpt-${VERSION}

RUN apt-get update && \
    apt-get install -y build-essential libjpeg62 \
    liblapack3 libceres1 jhead python3 python3-pil \
    python3-ruamel.yaml \
    rsync wget && \
    apt-get clean
    
WORKDIR /opt

RUN wget -q https://github.com/epassaro/linux-photogrammetry-tools/releases/download/${VERSION}/${BASENAME}.tar.gz && \
    tar zxf ${BASENAME}.tar.gz && \
    rm -f ${BASENAME}.tar.gz

WORKDIR /opt/${BASENAME}

CMD ["/bin/bash"]
