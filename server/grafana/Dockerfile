FROM grafana/grafana:5.4.3

USER root

WORKDIR /tmp

RUN grafana-cli plugins install grafana-piechart-panel \
  &&  grafana-cli plugins install grafana-worldmap-panel

ARG VERSION=""
ARG LANGUAGE

ENV VERSION $VERSION
ENV LANGUAGE $LANGUAGE

COPY ./dashboards /var/lib/grafana/dashboards
COPY language.ini /tmp/language.ini
COPY language.sh /tmp/language.sh

RUN bash /tmp/language.sh

# replace $VERSION_NUMBER mark in the dashboard config file with env variable $VERSION
RUN sed -i "s/\$VERSION_NUMBER/$VERSION/g" /var/lib/grafana/dashboards/SummaryDashboard.json
