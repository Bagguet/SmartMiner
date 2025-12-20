FROM ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    libuv1-dev \
    libssl-dev \
    libhwloc-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /xmrig_src

RUN git clone https://github.com/xmrig/xmrig.git . && \
    mkdir build && cd build && \
    cmake .. && make -j$(nproc)

FROM ubuntu:22.04

COPY --from=builder /xmrig_src/build/xmrig /usr/local/bin/xmrig

RUN apt-get update && apt-get install -y \
    libuv1 \
    libssl-dev \
    libhwloc-dev \
    msr-tools \ 
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["xmrig"]