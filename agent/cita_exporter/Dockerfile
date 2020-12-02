FROM rust:1.48 AS builder
WORKDIR /build
RUN curl -o musl-1.1.19.tar.gz https://www.musl-libc.org/releases/musl-1.1.19.tar.gz \
	&& tar -xzvf musl-1.1.19.tar.gz \
	&& cd musl-1.1.19/ \
	&& ./configure && make && make install \
	&& ln -sf /usr/local/musl/bin/musl-gcc /usr/local/bin/musl-gcc
COPY ./cita-cli.git /build/cita-cli.git
WORKDIR /build/cita-cli.git/cita-cli
RUN rustup target add x86_64-unknown-linux-musl \
	&& RUSTFLAGS='-A deprecated' cargo install --target x86_64-unknown-linux-musl --path .

FROM ubuntu:18.04 AS final
COPY --from=build /usr/local/cargo/bin/cita-cli /bin/cita-cli
RUN chmod +x /bin/cita-cli
WORKDIR /config
COPY ./cita_monitor_agent.py ./requirements.txt /config/
RUN apt-get update \
	&& apt-get install -y python3 python3-pip libcurl4-openssl-dev \
	&& apt-get clean \
	&& apt-get autoclean \
	&& rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt
ENV PORT=1923
CMD "python3" "cita_monitor_agent.py" "$NODE_IP_PORT" "$PORT" "$NODE_DIR"
