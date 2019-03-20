#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
import prometheus_client
from prometheus_client import Counter,Enum,Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask
import json
import os
import sys
##########
Node = sys.argv[1]
##########
NodeFlask = Flask(__name__)
##########
class Monitor_Function(object):
    def __init__(self, NodeIP, NodePort):
        self.NodeIP = NodeIP
        self.NodePort = NodePort
    def cita_cli_Request(self, payload):
        r = "timeout 3 cita-cli %s --url http://%s:%s" %(payload,self.NodeIP,self.NodePort)
        try:
            rResult = os.popen(r)
        except:
            return -99
        else:
            PayloadResult = json.loads(rResult.read())
            return PayloadResult
    def blockNumber(self):
        payload = "rpc blockNumber"
        return self.cita_cli_Request(payload)
    def peerCount(self):
        payload = "rpc peerCount"
        return self.cita_cli_Request(payload)
    def getBlockByNumber(self,Height):
        payload = "rpc getBlockByNumber --height %s" %(Height)
        return self.cita_cli_Request(payload)
    def getMetaData(self):
        payload = "rpc getMetaData"
        return self.cita_cli_Request(payload)
    def NodeManager_listNode(self):
        payload = "scm NodeManager listNode"
        return self.cita_cli_Request(payload)
##########
@NodeFlask.route("/metrics")
def Node_Get():
    CITA_Chain = CollectorRegistry(auto_describe=False)
    Node_Get_ServiceStatus = Gauge("Node_Get_ServiceStatus",
                                   "Get the running state of the script, return 1 when running; return 0 if it is not running;",
                                   ["NodeIP", "NodePort"],
                                   registry=CITA_Chain)
    Node_Get_FirstBlocknumberDetails = Gauge("Node_Get_FirstBlocknumberDetails",
                                             "Get the hash and timestamp of the first block;",
                                             ["NodeIP", "NodePort", "FirstBlocknumberHash"],
                                             registry=CITA_Chain)
    Node_Get_ChainInfo = Gauge("Node_Get_ChainInfo",
                               "Get basic information and economic model of CITA service running on the node;",
                               ["NodeIP", "NodePort", "ChainName", "Operator", "TokenName", "TokenSymbol", "Version"],
                               registry=CITA_Chain)
    Node_Get_NodePeers = Gauge("Node_Get_NodePeers",
                               "Get the number of node connections;",
                               ["NodeIP", "NodePort"],
                               registry=CITA_Chain)
    Node_Get_ChainNodes = Gauge("Node_Get_ChainNodes",
                                "Get the number of CITA service Consensus nodes;",
                                ["NodeIP", "NodePort"],
                                registry=CITA_Chain)
    Node_Get_LastBlocknumber = Gauge("Node_Get_LastBlocknumber",
                                     "Get the latest block height;",
                                     ["NodeIP", "NodePort", "FirstBlocknumberHash"],
                                     registry=CITA_Chain)
    Node_Get_LastBlocknumberDetails = Gauge("Node_Get_LastBlocknumberDetails",
                                            "Get the hash and timestamp of the last block;",
                                            ["NodeIP", "NodePort", "LastBlocknumber", "LastBlocknumberInt","LastBlocknumberHash"],
                                            registry=CITA_Chain)
    NodeIP = str(Node.split(':')[0])
    NodePort = str(Node.split(':')[1])
    Check_CITA_Process = os.popen("ps alx |grep 'cita-chain' |grep -c -v grep")
    if Check_CITA_Process.read() == '0\n':
        Node_Get_ServiceStatus.labels(NodeIP=NodeIP,NodePort=NodePort).set(0)
        return Response(prometheus_client.generate_latest(CITA_Chain), mimetype="text/plain")
    else:
        Node_Get_ServiceStatus.labels(NodeIP=NodeIP, NodePort=NodePort).set(1)
        GetResult = Monitor_Function(NodeIP, NodePort)
        Node_Get_FirstBlocknumberDetails_by_getBlockByNumber = GetResult.getBlockByNumber('0x0')
        if Node_Get_FirstBlocknumberDetails_by_getBlockByNumber != -99:
            FirstBlocknumberHash = Node_Get_FirstBlocknumberDetails_by_getBlockByNumber['result']['hash']
            FirstBlocknumberTimestamp = Node_Get_FirstBlocknumberDetails_by_getBlockByNumber['result']['header']['timestamp']
            Node_Get_FirstBlocknumberDetails.labels(NodeIP=NodeIP, NodePort=NodePort,FirstBlocknumberHash=FirstBlocknumberHash).set(FirstBlocknumberTimestamp)
        Node_Get_ChainInfo_by_getMetaData = GetResult.getMetaData()
        if Node_Get_ChainInfo_by_getMetaData != -99:
            ChainName = Node_Get_ChainInfo_by_getMetaData['result']['chainName']
            ChainOperator = Node_Get_ChainInfo_by_getMetaData['result']['operator']
            ChainTokenName = Node_Get_ChainInfo_by_getMetaData['result']['tokenName']
            ChainTokenSymbol = Node_Get_ChainInfo_by_getMetaData['result']['tokenSymbol']
            ChainEconomicalModel = Node_Get_ChainInfo_by_getMetaData['result']['economicalModel']
            ChainVersion = Node_Get_ChainInfo_by_getMetaData['result']['version']
            Node_Get_ChainInfo.labels(NodeIP=NodeIP, NodePort=NodePort, ChainName=ChainName, Operator=ChainOperator, TokenName=ChainTokenName, TokenSymbol=ChainTokenSymbol, Version=ChainVersion).set(ChainEconomicalModel)
        Node_Get_ChainNodes_by_NodeManager_listNode = GetResult.NodeManager_listNode()
        if Node_Get_ChainNodes_by_NodeManager_listNode != -99:
            ChainNodesInfo = Node_Get_ChainNodes_by_NodeManager_listNode['result']
            ChainNodesCount = (len(ChainNodesInfo.split('000000000000000000000000')) - 5)
            Node_Get_ChainNodes.labels(NodeIP=NodeIP, NodePort=NodePort).set(ChainNodesCount)
        Node_Get_LastBlocknumber_by_blockNumber = GetResult.blockNumber()
        if Node_Get_LastBlocknumber_by_blockNumber != -99:
            Blocknumber = Node_Get_LastBlocknumber_by_blockNumber['result']
            Node_Get_LastBlocknumber.labels(NodeIP=NodeIP, NodePort=NodePort, FirstBlocknumberHash=FirstBlocknumberHash).set(int(Blocknumber,16))
        Node_Get_LastBlocknumberDetails_by_getBlockByNumber = GetResult.getBlockByNumber(Blocknumber)
        if Node_Get_LastBlocknumberDetails_by_getBlockByNumber != -99:
            LastBlocknumberHash = Node_Get_LastBlocknumberDetails_by_getBlockByNumber['result']['hash']
            LastBlocknumberTimestamp = Node_Get_LastBlocknumberDetails_by_getBlockByNumber['result']['header']['timestamp']
            Node_Get_LastBlocknumberDetails.labels(NodeIP=NodeIP, NodePort=NodePort, LastBlocknumber=Blocknumber,LastBlocknumberInt=int(Blocknumber,16), LastBlocknumberHash=LastBlocknumberHash).set(LastBlocknumberTimestamp)
        Node_Get_NodePeers_by_peerCount = GetResult.peerCount()
        if Node_Get_NodePeers_by_peerCount != -99:
            NodePeers = Node_Get_NodePeers_by_peerCount['result']
            Node_Get_NodePeers.labels(NodeIP=NodeIP, NodePort=NodePort).set(int(NodePeers, 16) + 1)
    return Response(prometheus_client.generate_latest(CITA_Chain), mimetype="text/plain")
##########
@NodeFlask.route("/")
def index():
    NodeIP = str(Node.split(':')[0])
    NodePort = str(Node.split(':')[1])
    index_text = "<h2>访问 Metrics 路径获取数据采集信息<br><br><a href='http://" + NodeIP + ':' + sys.argv[2] + "/metrics'>点击跳转 Metrics</a></h2>"
    return index_text
##########
if __name__ == "__main__":
    NodeFlask.run(host="0.0.0.0", port=int(sys.argv[2]))
