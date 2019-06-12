FROM grafana/grafana:5.4.2

USER root

WORKDIR /tmp

RUN grafana-cli plugins install grafana-piechart-panel \
  &&  grafana-cli plugins install grafana-worldmap-panel

ARG VERSION=""

ENV VERSION $VERSION

COPY ./dashboards /var/lib/grafana/dashboards

#replace $VERSION_NUMBER mark in the dashboard config file with env variable $VERSION
RUN sed -i "s/\$VERSION_NUMBER/$VERSION/g" /var/lib/grafana/dashboards/SummaryDashboard.json
