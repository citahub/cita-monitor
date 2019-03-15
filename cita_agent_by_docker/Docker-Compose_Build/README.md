## CITA monitor 容器编排部署
 编排创建4个容器，分别是 prometheus_node_exporter、prometheus_process_exporter、prometheus_rabbitmq_exporter、prometheus_citaMonitorAgent_port1337_exporter
* prometheus_node_exporter
	* 监控主机资源
* prometheus_process_exporter
	* 监控指定进程资源
* prometheus_rabbitmq_exporter
	* 监控 rabbitmq 服务
* prometheus_citaMonitorAgent_port1337_exporter
	* 监控运行 cita 服务的 node 状态信息

---
### 部署命令
```
docker-compose up -d
```

### 可修改参数（修改 docker-compose.yml）
* prometheus_node_exporter
```
hostname:
container_name:
ports:
volumes:

entrypoint 或者 command 选择任意一个
```
* prometheus_process_exporter
```
hostname:
container_name:
ports:
volumes:
```
* 目录 process_exporter_config 下的配置文件 process_list.yml 格式如下：
```
process_names:
        - comm:
                - cita-forever
                - cita-network
                - cita-jsonrpc
                - cita-bft
                - cita-chain
                - cita-auth
                - cita-executor
```
* prometheus_rabbitmq_exporter
```
hostname:
container_name:
ports:
network_mode:
environment:
```
