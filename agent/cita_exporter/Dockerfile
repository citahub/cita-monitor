FROM ubuntu:18.04
WORKDIR /config
ADD . /config
RUN apt-get update \
  && apt-get install -y  \
	  python3 \
	  python3-pip \
	  libcurl4-openssl-dev \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt
RUN mv cita-cli /bin/cita-cli && chmod +x /bin/cita-cli
ENV PORT=1923
CMD "python3" "cita_monitor_agent.py" "$NODE_IP_PORT" "$PORT" "$NODE_DIR"
