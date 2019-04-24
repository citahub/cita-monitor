# CITA Monitor

## 概要
CITA Monitor 是将多个开源产品（`Prometheus`, `Grafana`）通过 `Docker` 部署和联动，从而实现对 `CITA` 服务的状态信息采集、展示和告警通知；
全套服务包含的开源产品如下：
* Prometheus
* Alertmanager
* Grafana
* Docker
* Python Script

## 示例


## 功能描述
### Agent
**目录 ./cita-monitor-agent**
* 提供了 `CITA` 服务采集脚本（`cita_monitor_agent.py`）
* 提供了 `docker-compose` 部署文件（`docker-compose.yml`）
* 提供了 Docker `image` 编译文件（`cita_exporter/Dockerfile`）
### Server
**目录 ./cita-monitor-server**
* 提供了 `docker-compose` 部署文件（`docker-compose.yml`）
* 提供了 `Grafana`、`Prometheus`、`Alertmanager` 配置文件
