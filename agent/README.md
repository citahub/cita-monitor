# Monitor Agent

## 概要
Monitor Agent 是使用 `Python` 作为脚本语言，使用 `cita-cli` 工具对 `CITA` 服务的状态进行查询，使用 `prometheus-client` 模块将数据格式化输出，使用 `Flask` 工具提供外部访问接口，将格式化后的数据直接进行展示；

## 部署
为了保证数据采集的基础环境一致性，数据采集进程均使用 `container` 部署;
### 容器编排部署
如果你希望采集关于运行 CITA 服务的主机资源更多的信息，你可以使用 `docker-compose` 来进行批量部署多个数据采集进程；
* prom/node-exporter （获取主机资源 | 参考: https://github.com/prometheus/node_exporter）
* ncabatoff/process-exporter （获取指定进程资源 | 参考: https://github.com/rberwald/process-exporter）
* kbudde/rabbitmq-exporter （获取rabbitmq 服务 | 参考: https://github.com/kbudde/rabbitmq_exporter）
* */cita-exporter:latest

#### 步骤
1、自定义采集信息
```
cp .env.example .env
vim .env

---

#采集端显示的主机名
hostname=nodehostname

#本地运行的 CITA 节点IP 和 Port
node_ip=1.1.1.1
node_Port=1337

#本地运行的 CITA 节点目录
node_dir=/data/cita_secp256k1_sha3/test-chain/0

#本地运行的 CITA 目录
soft_path=/data/cita_secp256k1_sha3/

#CITA 目录所在的磁盘挂载目录
disk_path=/data

#本地运行的 CITA 节点在链上的 node ID
node_id=0
```
2、启动进程
```
docker-compose up -d
```
3、查看数据采集信息
```
#prometheus_host_exporter
curl http://localhost:1920/metrics

#prometheus_process_exporter
curl http://localhost:1921/metrics

#prometheus_rabbitmq_exporter
curl http://localhost:1922/metrics

#prometheus_cita_exporter
curl http://localhost:1923/metrics
```
4、关闭进程
```
docker-compose down
```

### 单个容器部署
如果你希望只采集 CITA 服务的运行状态信息，你可以使用 `docker` 命令来运行一个数据采集进程；

#### 步骤
1、编译镜像
```
cd ./cita_exporter
docker build -t cita_exporter .
cd ..
```
2、启动容器
Tips：
请填入宿主机物理网卡 IP 地址，切勿使用 127.0.0.1，exporter 进程在容器中运行，127.0.0.1 将会导致访问容器本地端口
```
docker run -d --name="prometheus_cita_exporter__x.x.x.x_1337" \
--pid="host" \
-p 1923:1920 \
-v "/data/cita_secp256k1_sha3/test-chain/0":"/data/cita_secp256k1_sha3/test-chain/0" \
-v "/data/cita_secp256k1_sha3/":"/data/cita_secp256k1_sha3/" \
-v "`pwd`/cita_monitor_agent.py":"/config/cita_monitor_agent.py" \
-e Node="x.x.x.x:1337" \
-e Port=1920 \
-e Node_Dir="/data/cita_secp256k1_sha3/test-chain/0" \
cita_exporter
```
3、查看数据采集信息
```
#prometheus_cita_exporter
curl http://localhost:1923/metrics
```

### 错误信息
1、容器启动失败
* 使用 `docker-compose logs container-name` or `docker logs container-name` 查看容器错误信息，一般原因是参数传入有误

2、容器启动成功，但是查看数据为空
* 启动数据采集进程时，会检查本地是否运行 CITA 服务，如果没有运行 CITA 服务，则 `Node_Get_ServiceStatus` 标签返回数值为 0，其他标签为空
