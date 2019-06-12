FROM grafana/grafana:5.4.2

USER root

WORKDIR /tmp

RUN grafana-cli plugins install grafana-piechart-panel \
  &&  grafana-cli plugins install grafana-worldmap-panel

ARG VERSION=""

ENV VERSION $VERSION

COPY ./dashboards /var/lib/grafana/dashboards

#Replace the placeholder and enter the correct version information
RUN sed -i "s/\$VERSION_NUMBER/$VERSION/g" /var/lib/grafana/dashboards/SummaryDashboard.json
