ARG BENCHMARK_IMAGE
FROM ${BENCHMARK_IMAGE}

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y \
        jq \
        libgmp-dev \
        git \
        python3 \
        python3-distutils \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN opam install -y \
        batteries \
        menhir \
        ocamlbuild \
        ocamlfind \
        ocamlformat \
        z3 \
        zarith \
    && git clone --depth 1 https://github.com/kupl/LearnML.git /opt/LearnML \
    && sed -i 's/Z3/z3/g' /opt/LearnML/engine/_tags \
    && cd /opt/LearnML/engine \
    && ./build 

WORKDIR /workspace
COPY ./bin /opt/bin
ENV PATH="/opt/bin:${PATH}"
RUN export BUGGY_PATH=$(cat metadata.json | jq -r '.buggyPath') \
    && cp metadata.json ${BUGGY_PATH}/metadata.json \
    && cd ${BUGGY_PATH} \
    && export PROBLEM=$(cat metadata.json | jq -r '.id' | cut -d'-' -f1) \
    && cp -r /opt/LearnML/benchmarks/C/${PROBLEM} ${PROBLEM} \
    && if [ -f test.ml ]; then \
        sed -i 's/open Src//g' test.ml; \
    fi
