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
RUN cd $(cat metadata.json | jq '.buggyPath') \
    && if [ -f test.ml ]; then \
        sed -i 's/open Src//g' test.ml \
    done
