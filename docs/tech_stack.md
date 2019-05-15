# CITA-Monitor Tech Stack

## Framework

* Prometheus - multiple client, metrics collection, data querying, visualization, time series database, alerting manager, many integrations
* Grafana - Data virtualization

## Server

### Backend Service

* Framework: Prometheus
* Language: Go
* key components：
    * OpenTSDB Exporter

### Database Service

* Leveldb - TSDB

### Frontend Service

* Framework: Grafana
* Language: 
    * Go
    * Node.js
    * Reactjs

### Alerting Service

* Framework: Alertmanager
* Receivers:
    * Email
    * Slack
    * Wechat
    * webhook
    * [other receivers](https://prometheus.io/docs/alerting/configuration/#receiver)

## Agent

* Framework: Prometheus
* Language: Python 3.6
* Client: [client_python](https://github.com/prometheus/client_python)
* Key components：
    * [node_exporter](https://github.com/prometheus/node_exporter)
    * [Process exporter](https://github.com/ncabatoff/process-exporter)
    * [RabbitMQ exporter](https://github.com/kbudde/rabbitmq_exporter)

## Operation Server

* OS: Ubuntu 18.04LTS

## Deployment

* Docker

## Refs

* https://prometheus.io/docs/introduction/overview/
* https://prometheus.io/docs/instrumenting/exporters/

