# Monitor Agent

## 概要
Monitor Agent 是使用 `Python` 作为脚本语言，使用 `cita-cli` 工具对 `CITA` 服务的状态进行查询，使用 `prometheus-client` 模块将数据格式化输出，使用 `Flask` 工具提供外部访问接口，将格式化后的数据直接进行展示；

## 部署
为了保证数据采集的基础环境一致性，数据采集进程均使用 `docker` 方式部署;
### 容器编排部署
如果你希望采集关于运行 CITA 服务的主机资源更多的信息，你可以使用 `docker-compose` 来进行批量部署多个数据采集进程；
* prom/node-exporter （获取主机资源 | 参考: https://github.com/prometheus/node_exporter）
* ncabatoff/process-exporter （获取指定进程资源 | 参考: https://github.com/rberwald/process-exporter）
* kbudde/rabbitmq-exporter （获取rabbitmq 服务 | 参考: https://github.com/kbudde/rabbitmq_exporter）
* citamon/agent-cita-exporter

#### 步骤
1、自定义采集信息
```
cd agent
cp .env.example .env
修改 .env 配置文件中 HOSTNAME、NODE_IP、NODE_PORT、NODE_DIR、SOFT_PATH、CITA_NODENAME、CITA_CHAIN_ID、CITA_NETWORKPORT 为实际部署的信息
---

#采集端显示的主机名
HOSTNAME=CITA-Node0

#本地运行的 CITA 节点IP 和 Port
NODE_IP=192.168.1.100
NODE_PORT=1337

#本地运行的 CITA 节点目录
NODE_DIR=/data/cita_secp256k1_sha3/test-chain/0

#本地运行的 CITA 目录
SOFT_PATH=/data/cita_secp256k1_sha3/
```
2、启动agent容器
```
docker-compose up -d
```
**可选项**
```
注意：CITA目录下应当存在bin目录
启动 CITA 与 Agent 服务容器
docker-compose -f docker-compose.yml -f cita_with_agent.yml up -d
```
3、查看数据采集信息
```
#citamon_agent_host_exporter
curl http://localhost:1920/metrics/host

#citamon_agent_process_exporter
curl http://localhost:1920/metrics/process

#citamon_agent_rabbitmq_exporter
curl http://localhost:1920/metrics/rabbitmq

#citamon_agent_cita_exporter
curl http://localhost:1920/metrics/cita
```
4、关闭agent容器
```
docker-compose down
```

### 单个容器部署
如果你希望只采集 CITA 服务的运行状态信息，你可以使用 `docker` 命令来运行一个数据采集容器；

#### 步骤
1、编译镜像
```
cd ./cita_exporter
docker build -t citamon/agent-cita-exporter .
cd ..
```
2、启动容器
Tips：
请填入宿主机物理网卡 IP 地址，切勿使用 127.0.0.1，exporter 进程在容器中运行，127.0.0.1 将会导致访问容器本地端口，以下示例中x.x.x.x表示为本地宿主机内网IP；

示例：
```
docker run -d --name="citamon_agent_cita_exporter_1337" \
--pid="host" \
-p 1920:1923 \
-v /etc/localtime:/etc/localtime \
-v "/data/cita_secp256k1_sha3/":"/data/cita_secp256k1_sha3/" \
-v "/data/cita_secp256k1_sha3/test-chain/0":"/data/cita_secp256k1_sha3/test-chain/0" \
-v "`pwd`/cita_monitor_agent.py":"/config/cita_monitor_agent.py" \
-e NODE_IP_PORT="x.x.x.x:1337" \
-e NODE_DIR="/data/cita_secp256k1_sha3/test-chain/0" \
citamon/agent-cita-exporter
```
3、查看数据采集信息
```
#citamon_agent_cita_exporter
curl http://localhost:1920/metrics/cita
```

### 错误信息
1、容器启动失败
* 使用 `docker-compose logs container-name` or `docker logs container-name` 查看容器错误信息，一般原因是参数传入有误

2、容器启动成功，但是查看数据为空
* 启动数据采集进程时，会检查本地是否运行 CITA 服务，如果没有运行 CITA 服务，则 `Node_Get_ServiceStatus` 标签返回数值为 0，其他标签为空
