# CITA-Monitor 服务端部署说明

## 服务端防火墙需要开通端口
```
1919 grafana
9093 alertmanager
9090 prometheus
自定义端口可在server根目录修改.env
```

## 获取源码 
```
cd /data/
git clone https://github.com/cryptape/cita-monitor.git
```

## 修改prometheus.yml 中默认的Job(node_exporter、rabbitmq_exporter、process_exporter、citaMonitorAgent_exporter)地址为CITA 节点IP地址
```
cd cita-monitor/CITA_Monitor_Server_Docker
vim config/prometheus.yml 
```
## 启动服务端
```
docker-compose up -d 
```
## 访问
````
Prometheus Console
http://127.0.0.1:9090
当agent启动后在 Prometheus Console 搜索Node_Get_LastBlocknumber 点击Execute可以看到块高
Prometheus Alertmanager
http://127.0.0.1:9093

Grafana
http://127.0.0.1:1919
默认账号：admin
默认密码：admin
```