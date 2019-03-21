## CITA monitor 容器编排部署
 编排创建4个容器，分别是 prometheus_node_exporter、prometheus_process_exporter、prometheus_rabbitmq_exporter、prometheus_citaMonitorAgent_port1337_exporter
* prometheus_node_exporter
	* 监控主机资源 | 参考: https://github.com/prometheus/node_exporter
* prometheus_process_exporter
	* 监控指定进程资源 | 参考: https://github.com/rberwald/process-exporter
* prometheus_rabbitmq_exporter
	* 监控 rabbitmq 服务 | 参考: https://github.com/kbudde/rabbitmq_exporter
* prometheus_citaMonitorAgent_exporter
	* 监控运行 cita 服务的 node 状态信息 | 参考: https://github.com/cryptape/cita-monitor/tree/docker_feature/CITA_Monitor_Agent_Docker/DockerImage_Build_Files

---
### 启动命令
```
docker-compose up -d
```

### 停止命令
```
docker-compose down
```

### 可修改参数（修改 .env 文件）
* 在 target ip 和 port 变量中填写监控的目标 CITA node 信息；
* 目录 process_exporter_config 下的配置文件 process_list.yml 格式如下,建议阅读原文：
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

### 访问采集数据（填入宿主机IP）
* prometheus_node_exporter
	* `http://*.*.*.:9100`
* prometheus_process_exporter
	* `http://*.*.*.:9256`
* prometheus_rabbitmq_exporter
	* `http://*.*.*.:9419`
* prometheus_citaMonitorAgent_exporter
	* `http://*.*.*.:1920`
	
### 建议
修改容器 hostname ，便于在面板中查看
