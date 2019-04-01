#!/bin/bash
#
Hostname=`hostname`
NodeIP=`ifconfig eth0|grep "inet addr:"|awk -F":" '{print $2}'|awk '{print $1}'`
#NodeIP=`ifconfig ens32|grep "inet"|head -n 1 |awk -F" " '{print $2}'|awk '{print $1}'`
OtherNode=1

install_agent(){
    cd ./CITA_Monitor_Agent_Docker/DockerCompose_Files
    sed -i "s/1.1.1.1/${NodeIP}/g" .env
    sed -i "s/nodehostname/${Hostname}/g" .env
    docker-compose up -d
    docker ps
}

install_server(){
    cd ../../CITA_Monitor_Server_Docker
    sed -i "s/1.1.1.1/${NodeIP}/g" ./config/prometheus.yml 
    docker-compose up -d
    docker ps
}

install_agent
sleep 5
install_server

check_container=`curl -I -m 10 -o /dev/null -s -w %{http_code} ${NodeIP}:1920`

if [[ ${check_container} -eq 200 ]]
then
    echo "Agent 安装成功"
    if  [[ ${OtherNode} -eq 1 ]]
    then
        echo "启动其他 node 监控"
        docker run -d --name="prometheus_citaMonitorAgent_exporter__${NodeIP}_1338" \
--pid="host" \
-p 1921:1920 \
-v "/data2/cita_secp256k1_sha3/test-chain/1":"/data2/cita_secp256k1_sha3/test-chain/1" \
-e Node="${NodeIP}:1338" \
-e Dir="/data2/cita_secp256k1_sha3/test-chain/1" \
-e NodeID=1 \
blankwu/cita_agent_by:cita-cli

	docker run -d --name="prometheus_citaMonitorAgent_exporter__${NodeIP}_1339" \
--pid="host" \
-p 1922:1920 \
-v "/data2/cita_secp256k1_sha3/test-chain/2":"/data2/cita_secp256k1_sha3/test-chain/2" \
-e Node="${NodeIP}:1339" \
-e Dir="/data2/cita_secp256k1_sha3/test-chain/2" \
-e NodeID=2 \
blankwu/cita_agent_by:cita-cli

	docker run -d --name="prometheus_citaMonitorAgent_exporter__${NodeIP}_1340" \
--pid="host" \
-p 1923:1920 \
-v "/data2/cita_secp256k1_sha3/test-chain/3":"/data2/cita_secp256k1_sha3/test-chain/3" \
-e Node="${NodeIP}:1340" \
-e Dir="/data2/cita_secp256k1_sha3/test-chain/3" \
-e NodeID=3 \
blankwu/cita_agent_by:cita-cli
    else
        echo "不启动其他 node 监控"
    fi
else
    echo "Agent 安装失败"
fi
