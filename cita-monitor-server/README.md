# CITA-Monitor 服务端部署说明

## 获取源码 
```
cd /data/
git clone https://jiangxianliang@bitbucket.org/cryptape/cita-monitor.git
```

## 修改prometheus.yml 中默认的agent节点ip为监控客户端服务器IP地址
```

sed -i "s/172.24.7.210/监控客户端服务器IP地址/g" prometheus/prometheus.yml 
```
## 启动服务端
```
docker-compose up -d 
```
## 访问
````
Prometheus Console
http://127.0.0.1:9090
当agent启动后在 Prometheus Console 搜索cita_blockMumber 点击Execute可以看到块高
Prometheus Alertmanager
http://127.0.0.1:9093

Grafana
http://127.0.0.1:1919
默认账号：admin
默认密码：admin
```