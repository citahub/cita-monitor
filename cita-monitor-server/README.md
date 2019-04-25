# Monitor Server

## 概要
Monitor Server 是使用容器编排的方式来批量创建和启动 `Prometheus`、`Alertmanager`、`Grafana` 的容器服务；

**数据获取流程**
1、`Prometheus` 定时请求 Agent 的 `Flask` 进程接口，获取实时的 CITA 服务信息，并存储到本地
2、通过 `Prometheus` 的 `alert` 规则，联动 `Alertmanager` 服务实现阈值触发后邮件告警
3、`Grafana` 服务定时请求 `Prometheus` 数据库 `API` 接口，将请求到的数据进行可视化展示

## 部署
首先在 `./config` 目录下，对相关服务进行自定义配置，使用 `docker-compose` 命令运行 `docker-compose.yml`，批量启动服务，如果对单个服务的配置进行调整，可以手动执行 `docker restart container-name` 来应用配置变更；

### 步骤
1、自定义服务运行端口
```
cp .env.example .env
vim .env
```
2、自定义服务配置文件
```
cd ./config

#Prometheus 配置文件
vim prometheus.yml

#Prometheus 告警规则配置文件
vim alert.rules

#Alertmanager 配置文件
vim alertmanager.yml

cd grafana

#Grafana 配置文件
vim grafana.ini

cd ../..
```
3、启动服务
```
docker-compose up -d
```
4、查看服务运行状态
```
docker ps

web 访问：
Grafana（默认密码 : admin/admin）
http://*.*.*.*:1919

Prometheus
http://*.*.*.*:1918

Alertmanager
http://*.*.*.*:1917
```
### 错误信息
1、容器启动失败
* 使用 `docker logs container-name` 查看容器错误信息，一般原因是参数传入有误

2、无法打开 `Grafana` 页面
* `Grafana` 启动时会安装组件，根据网络质量情况需要等等 2-5 分钟

3、`Prometheus` 没有采集到数据
* 请查看 `Prometheus` 的配置文件，是否配置了正确的 Agent IP 和进程 Port
* 请排查 Server 和 Agent 的防火墙配置信息，是否放行了相关进程或服务端口

4、`Grafana` 面板报错
* 默认提供了 `dashboard` 文件，请在 `config/dashboards` 下查看文件是否存在
* 查看 `Prometheus` 数据采集是否正常
