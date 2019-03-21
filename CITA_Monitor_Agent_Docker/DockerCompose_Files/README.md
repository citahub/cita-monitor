## CITA monitor 容器编排部署
 编排创建4个容器，分别是 prometheus_node_exporter、prometheus_process_exporter、prometheus_rabbitmq_exporter、prometheus_citaMonitorAgent_port1337_exporter
* prometheus_node_exporter
	* 监控主机资源 | 参考: https://github.com/prometheus/node_exporter
* prometheus_process_exporter
	* 监控指定进程资源 | 参考: https://github.com/rberwald/process-exporter
* prometheus_rabbitmq_exporter
	* 监控 rabbitmq 服务 | 参考: https://github.com/kbudde/rabbitmq_exporter
* prometheus_citaMonitorAgent_port1337_exporter
	* 监控运行 cita 服务的 node 状态信息 | 参考: https://github.com/cryptape/cita-monitor/tree/dev_test/cita_agent_by_docker/DockerFile_Build

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
* prometheus_citaMonitorAgent_port1337_exporter
```
hostname:
container_name:
ports:
environment:

请在 environment 下的变量中填写监控的目标节点信息
Node=IP:Port
OpenPort=映射的端口，默认1920
```

### 访问端口
* prometheus_node_exporter
	* `http://*.*.*.:9100`
* prometheus_process_exporter
	* `http://*.*.*.:9256`
* prometheus_rabbitmq_exporter
	* `http://*.*.*.:9419`
* prometheus_citaMonitorAgent_port1337_exporter
	* `http://*.*.*.:1920`
	
### 建议
修改容器 hostname ，便于在面板中查看
