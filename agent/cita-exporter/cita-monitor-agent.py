#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
import prometheus_client
from prometheus_client import Counter,Enum,Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import json
import requests
import os
import platform
import geohash
import psutil
import threading
##########
NodeLists = {'127.0.0.1':'1337'}
##########
#Router list
ChainInfos = Flask(__name__)
NodeInfos = Flask(__name__)
HostInfos = Flask(__name__)
##########
#Lables registry
ChainInfo = CollectorRegistry(auto_describe=False)
NodeInfo = CollectorRegistry(auto_describe=False)
HostInfo = CollectorRegistry(auto_describe=False)
CITA_ChainInfo_Services_Status = Gauge("CITA_ChainInfo_Services_Status", "Null", ["ServicesStatus"], registry=ChainInfo)
CITA_NodeInfo_Services_Status = Gauge("CITA_NodeInfo_Services_Status", "Null", ["ServicesStatus"], registry=NodeInfo)
CITA_HostInfo_Services_Status = Gauge("CITA_HostInfo_Services_Status", "Null", ["ServicesStatus"], registry=HostInfo)
##########
#Lables
ChainInfo_FirstBlocknumber_timestamp = Gauge("ChainInfo_FirstBlocknumber_timestamp","Null",["NodeIp", "NodePort", "FirstBlocknumberHash"],registry=ChainInfo)
ChainInfo_ChainMetaData_blockInterval = Gauge("ChainInfo_ChainMetaData_simple","Null",["NodeIp", "NodePort", "FirstBlocknumberHash", "chainName", "operator", "tokenName", "tokenSymbol"],registry=ChainInfo)
ChainInfo_ChainMetaData_timestamp = Gauge("ChainInfo_ChainMetaData_timestamp","Null",["NodeIp", "NodePort", "FirstBlocknumberHash", "economicalModel", "validators"],registry=ChainInfo)
ChainInfo_ChainPeerCounts_consensus = Gauge("ChainInfo_ChainPeerCounts_consensus","Null",["NodeIp", "NodePort", "FirstBlocknumberHash"],registry=ChainInfo)
ChainInfo_InstanceLocation = Gauge("ChainInfo_InstanceLocation","Null",["NodeIp", "NodePort", "FirstBlocknumberHash", "PublicIP", "hostNation", "hostProvince", "hostCity", "hostGeohash"],registry=ChainInfo)
#
NodeInfo_LastBlocknumber = Gauge("NodeInfo_LastBlocknumber","Null",["NodeIp", "NodePort"],registry=NodeInfo)
NodeInfo_LastBlocknumber_timestamp = Gauge("NodeInfo_LastBlocknumber_timestamp","Null",["NodeIp", "NodePort"],registry=NodeInfo)
NodeInfo_NodePeerCounts_full = Gauge("NodeInfo_NodePeerCounts_full","Null",["NodeIp", "NodePort"],registry=NodeInfo)
#
HostInfo_CPU = Gauge("HostInfo_CPU","Null",["NodeIp", "NodePort"],registry=HostInfo)
HostInfo_Disk = Gauge("HostInfo_Disk","Null",["diskName"],registry=HostInfo)
HostInfo_CPU_process = Gauge("HostInfo_CPU_process","Null",["processName"],registry=HostInfo)
HostInfo_Memory_process = Gauge("HostInfo_Memory_process","Null",["processName"],registry=HostInfo)
HostInfo_simple = Gauge("HostInfo_simple","Null",["hostName", "systemPlatform"],registry=HostInfo)
##########
class Monitor_Function(object):
##########
#基础功能
    def __init__(self, NodeIp, NodePort):
        self.NodeIp = NodeIp
        self.NodePort = NodePort
#
    def cita_cli_Request(self, payload):
        r = "timeout 3 cita-cli %s --url http://%s:%s" %(payload,self.NodeIp,self.NodePort)
        try:
            rResult = os.popen(r)
        except:
            return -99
        else:
            PayloadResult = json.loads(rResult.read())
            return PayloadResult
#
    def getLocalHost_citaProcess(self, type, pid):
        try:
            id = psutil.Process(pid)
        except psutil.NoSuchProcess:
            return -99
        else:
            if type == 'CPU':
                return id.cpu_percent()
            elif type == 'Memory':
                ProcessMemoryInfo = list(id.memory_info())
                return ProcessMemoryInfo[0]
##########
# cita-cli 命令
#返回 json 格式数据
    def blockMumber(self):
        payload = "rpc blockNumber"
        return self.cita_cli_Request(payload)
#
    def peerCount(self):
        payload = "rpc peerCount"
        return self.cita_cli_Request(payload)
#
    def getBlockByNumber(self,Height):
        payload = "rpc getBlockByNumber --height %s" %(Height)
        return self.cita_cli_Request(payload)
#
    def getMetaData(self):
        payload = "rpc getMetaData"
        return self.cita_cli_Request(payload)
#
    def NodeManager_listNode(self):
        payload = "scm NodeManager listNode"
        return self.cita_cli_Request(payload)
##########
#获取 IP 信息
    def getPublicIp(self):
        url = 'https://api.Ipify.org'
        try:
            r = requests.get(url, timeout=3)
        except:
            return -99
        else:
            return r.text
#
    def getPublicIpLocation(self, Ipaddress, LocationKey):
        url = 'https://apis.map.qq.com/ws/location/v1/ip?ip=%s&key=%s' %(Ipaddress,LocationKey)
        try:
            r = requests.get(url, timeout=3)
        except:
            return -99
        else:
            if r.json()['message'] == 'query ok' :
                return r.json()
            else:
                return -99
##########
@ChainInfos.route("/metrics")
def startChainInfos():
    check_cita = os.popen("ps aux | grep -c 'cita-jsonrpc'")
    if check_cita.read() == '1\n':
        CITA_ChainInfo_Services_Status.labels(ServicesStatus='Down').set(0)
        return Response(prometheus_client.generate_latest(ChainInfo), mimetype="text/plain")
    else:
        for NodeIp, NodePort in NodeLists.items():
            GetResult =  Monitor_Function(NodeIp, NodePort)
            # * ChainInfo_FirstBlocknumber_timestamp
            FirstBlocknumberInfo = GetResult.getBlockByNumber('0x0')
            if FirstBlocknumberInfo != -99:
                FirstBlocknumberHash = FirstBlocknumberInfo['result']['hash']
                FirstBlocknumber_timestamp = FirstBlocknumberInfo['result']['header']['timestamp']
                ChainInfo_FirstBlocknumber_timestamp.labels(NodeIp=NodeIp, NodePort=NodePort, FirstBlocknumberHash=FirstBlocknumberHash).set(FirstBlocknumber_timestamp)
            # * ChainInfo_ChainMetaData_blockInterval
            # * ChainInfo_ChainMetaData_timestamp
            ChainMetaDataInfo = GetResult.getMetaData()
            if ChainMetaDataInfo != -99:
                ChainName = ChainMetaDataInfo['result']['chainName']
                ChainOperator = ChainMetaDataInfo['result']['operator']
                ChainTokenName = ChainMetaDataInfo['result']['tokenName']
                ChainTokenSymbol = ChainMetaDataInfo['result']['tokenSymbol']
                ChainBlockInterval = ChainMetaDataInfo['result']['blockInterval']
                ChainEconomicalModel = ChainMetaDataInfo['result']['economicalModel']
                ChainGenesisTimestamp = ChainMetaDataInfo['result']['genesisTimestamp']
                ChainValidators = ChainMetaDataInfo['result']['validators']
                ChainVersion = ChainMetaDataInfo['result']['version']
                ChainInfo_ChainMetaData_blockInterval.labels(NodeIp=NodeIp, NodePort=NodePort, FirstBlocknumberHash=FirstBlocknumberHash, chainName=ChainName, operator=ChainOperator, tokenName=ChainTokenName, tokenSymbol=ChainTokenSymbol).set(ChainBlockInterval)
                ChainInfo_ChainMetaData_timestamp.labels(NodeIp=NodeIp, NodePort=NodePort, FirstBlocknumberHash=FirstBlocknumberHash, economicalModel=ChainEconomicalModel, validators=ChainValidators).set(ChainGenesisTimestamp)
            # * ChainInfo_NodePeerCounts_consensus
            NodePeerCounts_consensus = GetResult.NodeManager_listNode()
            if NodePeerCounts_consensus != -99:
                ConsensusInfo = NodePeerCounts_consensus['result']
                ConsensusCount = (len(ConsensusInfo.split('000000000000000000000000')) - 5)
                ChainInfo_ChainPeerCounts_consensus.labels(NodeIp=NodeIp, NodePort=NodePort, FirstBlocknumberHash=FirstBlocknumberHash).set(ConsensusCount)
            # * ChainInfo_NodeLocation
            publicIp = GetResult.getPublicIp()
            if publicIp != -99:
                LocationKey = '2OBBZ-MX3CU-MUYVA-BGI7X-PEXYQ-UBBLJ'
                NodeLocationInfo = GetResult.getPublicIpLocation(publicIp, LocationKey)
                if NodeLocationInfo != -99:
                    InstaceNation = NodeLocationInfo['result']['ad_info']['nation']
                    InstaceProvince = NodeLocationInfo['result']['ad_info']['province']
                    InstaceCity = NodeLocationInfo['result']['ad_info']['city']
                    InstaceGeohash = geohash.encode(NodeLocationInfo['result']['location']['lat'],NodeLocationInfo['result']['location']['lng'])
                    ChainInfo_InstanceLocation.labels(NodeIp=NodeIp, NodePort=NodePort, FirstBlocknumberHash=FirstBlocknumberHash, PublicIP=publicIp, hostNation=InstaceNation, hostProvince=InstaceProvince, hostCity=InstaceCity, hostGeohash=InstaceGeohash).set(1)
    return Response(prometheus_client.generate_latest(ChainInfo), mimetype="text/plain")
#
@NodeInfos.route("/metrics")
def startNodeInfos():
    check_cita = os.popen("ps aux | grep -c 'cita-jsonrpc'")
    if check_cita.read() == '1\n':
        CITA_NodeInfo_Services_Status.labels(ServicesStatus='Down').set(0)
        return Response(prometheus_client.generate_latest(NodeInfo), mimetype="text/plain")
    else:
        for NodeIp, NodePort in NodeLists.items():
            GetResult= Monitor_Function(NodeIp,NodePort)
            # * NodeInfo_LastBlocknumber
            LastBlocknumber = GetResult.blockMumber()
            if LastBlocknumber != -99:
                Blocknumber = LastBlocknumber['result']
                NodeInfo_LastBlocknumber.labels(NodeIp=NodeIp, NodePort=NodePort).set(int(Blocknumber,16))
            # * NodeInfo_LastBlocknumber_timestamp
            LastBlocknumberInfo = GetResult.getBlockByNumber(Blocknumber)
            if LastBlocknumberInfo != -99:
                LastBlocknumberHash = LastBlocknumberInfo['result']['hash']
                LastBlocknumberTimestamp = LastBlocknumberInfo['result']['header']['timestamp']
                NodeInfo_LastBlocknumber_timestamp.labels(NodeIp=NodeIp, NodePort=NodePort).set(LastBlocknumberTimestamp)
            # * NodeInfo_NodePeerCounts_full
            NodePeerCounts_full = GetResult.peerCount()
            if NodePeerCounts_full != -99:
                PeerCounts_full = NodePeerCounts_full['result']
                NodeInfo_NodePeerCounts_full.labels(NodeIp=NodeIp, NodePort=NodePort).set(int(PeerCounts_full,16) + 1)
    return Response(prometheus_client.generate_latest(NodeInfo), mimetype="text/plain")

@HostInfos.route("/metrics")
def startHostInfos():
    check_cita = os.popen("ps aux | grep -c 'cita-jsonrpc'")
    if check_cita.read() == '1\n':
        CITA_HostInfo_Services_Status.labels(ServicesStatus='Down').set(0)
        return Response(prometheus_client.generate_latest(HostInfo), mimetype="text/plain")
    else:
        for NodeIp, NodePort in NodeLists.items():
            for cita_id in psutil.pids():
                try:
                    id = psutil.Process(cita_id)
                except psutil.NoSuchProcess:
                    pass
                else:
                    if 'cita-' in id.name() or 'rabbitmq' in id.name():
                        if id.name() != 'cita-cli':
                            ProcessName = (str(id.name()) + '_pid:' + str(cita_id))
                            ProcessMemoryInfo = list(id.memory_info())
                            HostInfo_CPU_process.labels(processName=ProcessName).set(id.cpu_percent())
                            HostInfo_Memory_process.labels(processName=ProcessName).set(ProcessMemoryInfo[0])
            uptime_exec = os.popen("uptime -s")
            uptimeformat = ("date +%s -d '" + uptime_exec.read().split('\n')[0] + "'")
            uptime = os.popen(uptimeformat)
            uptime = uptime.read().split('\n')[0]
            HostInfo_simple.labels(hostName=platform.node(), systemPlatform=platform.platform()).set(int(uptime))
            HostInfo_CPU.labels(NodeIp=NodeIp, NodePort=NodePort).set(psutil.cpu_percent())
            HostInfo_Disk.labels(diskName="'/'").set(list(psutil.disk_usage('/'))[-1])
    return Response(prometheus_client.generate_latest(HostInfo),mimetype="text/plain")
##########
if __name__ == "__main__":
    t1 = threading.Thread(target=ChainInfos.run,args=("0.0.0.0",1921))
    t2 = threading.Thread(target=NodeInfos.run, args=("0.0.0.0",1922))
    t3 = threading.Thread(target=HostInfos.run, args=("0.0.0.0",1923))
    t1.start()
    t2.start()
    t3.start()
