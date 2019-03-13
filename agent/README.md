# CITA-Monitor 客户端部署说明

## 获取源码 
```
cd /data/
git clone https://jiangxianliang@bitbucket.org/cryptape/cita-monitor.git
```

## 启动客户端
```
cd cita-monitor/agent
docker-compose up -d 
```
## 查看节点数据
```
node-exporter
http://127.0.0.1:9100

cita_exporter
http://127.0.0.1:1921/metrics
```
