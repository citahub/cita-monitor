FROM python:3

COPY requirements.txt /
COPY cita-monitor-agent.py /

RUN pip install -r /requirements.txt

ADD https://cdn.cryptape.com/cita-cli /usr/bin/

RUN chmod +x /usr/bin/cita-cli

EXPOSE 1921 1922 1923

CMD [ "python", "./cita-monitor-agent.py" ]
