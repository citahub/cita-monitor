# CITA-Monitor

[EN](README.md) | [CN](README-CN.md)

A Prometheus project to monitor running status of [CITA](https://github.com/cryptape/cita).

Metrics are including blockchain data, process status, host info like CPU/memory/disk usage etc.

## Screenshots for Dashboards

Summary Dashboard Demo
![summary-dashboard-demo-fs8](https://user-images.githubusercontent.com/71397/57682153-b9a5c700-7663-11e9-93c6-a29758e7d3a1.png)

CITA Node Info Dashboard Demo
![cita-node-info-dashboard-demo-fs8](https://user-images.githubusercontent.com/71397/57681838-15bc1b80-7663-11e9-91b4-202c306a0f3b.png)

Host Info Dashboard Demo
![host-info-dashboard-demo-fs8](https://user-images.githubusercontent.com/71397/57681906-3ab08e80-7663-11e9-9229-76b85c0eaaa4.png)

Rabbitmq Dashboard Demo
![rabbitmq-dashboard-demo-fs8](https://user-images.githubusercontent.com/71397/57682140-b0b4f580-7663-11e9-8db0-c4e2a0e29606.png)


## Feature List

* CITA 服务进程监控
    - CITA 微服务及MQ进程的存活、进程的CPU、内存使用率、IO
* 区块链数据健康监控
    - 节点出块高度历史、出块时间、出块间隔趋势、Quota、交易量历史、TPS、磁盘占用比例、数据目录大小增长趋势
* 运行环境监控
    - 主机运行环境的系统负载、CPU、内存、磁盘空间使用情况、网络流量、TCP连接数等
* 故障告警通知
    - [监控告警策略](docs/alert_strategies.md)
    - 支持邮件通知、Slack通知、短信通知（Pro 版）
* 节点网络监控（Pro 版）
    - 连接节点数、网络拓扑、地理位置等
* 鉴源限流（Pro 版）
    - 鉴别请求来源、工具；限制访问来源、频率
* JSONRPC 接口调用分析（Pro 版）
    - 统计分析RPC方法的请求时间、请求次数

### Metrics of Dashboards

* Summary Dashboard
    * 各节点最新块高
    * 各节点监控进程存活
    * 各节点CPU使用率变化
    * 节点列表
* CITA Node Info Dashboard
    * CITA Meta Data - 链的配置信息，如 Chain Name、创建时间等
    * Chain Info - 链的最新块高、共识节点数、共识节点出块历史趋势
    * Node Info - 选定节点的详细信息，包括区块链数据、运行环境、运行软件信息
* Host Info Dashboard
    * 各节点运行主机的信息，包括系统负载、CPU、内存、硬盘使用率、网络流量
* Process Info Dashboard
    * 节点中 CITA 微服进程的存活历史、CPU、内存、IO变化历史
* RabbitMQ Dashboard
    * RabbitMQ 服务的存活状态、channels 、consumers、connections、queues 等的变化记录

更细节可查看：[监控指标信息结构](docs/information_architecture.md)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

* Docker: [install Docker guide](https://docs.docker.com/install/)
* Python: [install Python guide](https://docs.python-guide.org/starting/installation/)

### Installing

for installing server, read [server/README.md](server/README.md)

for installing agent, read [agent/README.md](agent/README.md)


## System Architecture

![](docs/imgs/CITA_Monitor_system_architecture-fs8.png)


### Ports default config

* CITA-Monitor server
    * Prometheus Alertmanager: 1917
    * Prometheus Console: 1918
    * Grafana: 1919
* CITA-Monitor agent
    * host_exporter：1920
    * process_exporter：1921
    * rabbitmq_exporter：1922
    * cita_exporter：1923 


## Contributing

### Creating a Bug Report

open a new issue: https://github.com/cryptape/cita-monitor/issues/new 

with your version info

### Tech Stack

Read [docs/tech_stack.md](docs/tech_stack.md) to know the programming languages, frameworks, and tools that developers use to build this software.

### Get source

```
git clone git@github.com:cryptape/cita-monitor.git
```

### Coding style

#### Coding style for Shell

* coding style guide: [Google Shell Style guide](https://google.github.io/styleguide/shell.xml)
* code formatter: [`shfmt -i 2 -ci`](https://github.com/mvdan/sh#shfmt), vscode extension: shell-format
* linter: [ShellCheck](https://github.com/koalaman/shellcheck), vscode extension: shell-format


#### Coding style for Python

* coding style guide: http://google.github.io/styleguide/pyguide.html
* code formatter: [yapf](https://github.com/google/yapf)
* linter: [pylint](https://www.pylint.org/)

#### Coding style for Docker

* coding style guide: https://github.com/Haufe-Lexware/docker-style-guide
* formatter: https://www.fromlatest.io/
* best-practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

#### Coding style for Makefile

* coding style guide: https://style-guides.readthedocs.io/en/latest/makefile.html
* tutorial: https://makefiletutorial.com/
* conventions: https://www.gnu.org/prep/standards/html_node/Makefile-Conventions.html
* best-practices: https://suva.sh/posts/well-documented-makefiles/

### Running the tests

PENDING: Explain how to run the automated tests for this system


### Commit your changes

#### Workflow

[GitHub Flow](https://help.github.com/en/articles/github-flow), [Understanding the GitHub flow](https://guides.github.com/introduction/flow/)

#### git style guide

use [git-style-guide](https://github.com/agis/git-style-guide) for Branches, Commits,Messages, Merging

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## License

This project is licensed under the Apache 2.0 License

## Acknowledgments

* Prometheus: https://prometheus.io/
* Prometheus node-exporter: https://github.com/prometheus/node_exporter
* Prometheus process-exporter: https://github.com/ncabatoff/process-exporter
* Prometheus rabbitmq-exporter: https://github.com/kbudde/rabbitmq_exporter
* CITA: http://docs.citahub.com
* Docker: https://www.docker.com/
