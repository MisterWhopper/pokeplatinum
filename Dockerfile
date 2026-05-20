FROM debian:trixie

RUN apt update -y && \
    apt install -y bison flex g++ gcc-arm-none-eabi git make ninja-build pkg-config wget python3 xz-utils nasm gcc-multilib;

RUN mkdir -p /app;

VOLUME ["/app"]
WORKDIR /app

CMD ["make"]
