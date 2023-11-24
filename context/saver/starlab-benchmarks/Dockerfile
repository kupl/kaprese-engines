ARG BENCHMARK_IMAGE
FROM ${BENCHMARK_IMAGE}

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y \
        build-essential \
        git \
        jq \
        libtinfo5 \
        libz3-dev \
        python \
        python3 \
        tzdata \
        wget \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/list/*

WORKDIR /opt
RUN wget https://github.com/kupl/SAVER_public/releases/download/saver/SAVER-1.0-SR.tar.gz -O saver.tar.gz \
    && tar -xvf saver.tar.gz \
    && rm saver.tar.gz

ENV PATH=/opt/saver-1.0/infer/bin:${PATH}

WORKDIR /workspace
COPY ./scripts/ /tmp/scripts/
RUN python3 /tmp/scripts/bootstrap.py metadata.json \
    && rm -rf /tmp/scripts
