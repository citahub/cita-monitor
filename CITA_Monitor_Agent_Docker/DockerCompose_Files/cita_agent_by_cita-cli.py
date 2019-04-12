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
import platform
import re
import psutil
##########
Node = sys.argv[1]
receive_path = sys.argv[3]
node_id = sys.argv[4]
soft_path = sys.argv[5]
disk_path = sys.argv[6]
##########
NodeFlask = Flask(__name__)
HostPlatform = platform.platform()
HostName = platform.node()
GetSoftVersion_txt = '%s/bin/cita-chain -V' %(soft_path)
try:
    GetSoftVersion_exec = os.popen(GetSoftVersion_txt)
    SoftVersion = str(GetSoftVersion_exec.read().split(' ')[1].split('\n')[0])
except:
    SoftVersion = 'null'
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
    def NodeDir_analysis(self, dir_path):
        global TotalFileSize
        global NodeAddress
        global NodeDisk
        address = "cat %s/address" %(dir_path)
        addressResult = os.popen(address)
        NodeAddress = str(addressResult.read().split('0x')[1].split('\n')[0])
        NodeDisk = psutil.disk_usage(disk_path).total
        TotalFileSize_txt = "cd %s && du | tail -n 1 | awk '{print $1}'" %(dir_path)
        try:
            TotalFileSize_exec = os.popen(TotalFileSize_txt)
            TotalFileSize = TotalFileSize_exec.read().split('\n')[0]
        except:
            TotalFileSize = 0
##########
@NodeFlask.route("/metrics")
def Node_Get():
    CITA_Chain = CollectorRegistry(auto_describe=False)
    Node_Get_ServiceStatus = Gauge("Node_Get_ServiceStatus",
                                   "Check local running cita services, value return 1 when running; return 0 is not running;",
                                   ["NodeIP", "NodePort"],
                                   registry=CITA_Chain)
    Node_Get_FirstBlocknumberDetails = Gauge("Node_Get_FirstBlocknumberDetails",
                                             "Get the hash and timestamp of the first block, value is timestamp;",
                                             ["NodeIP", "NodePort", "FirstBlocknumberHash"],
                                             registry=CITA_Chain)
    Node_Get_ChainInfo = Gauge("Node_Get_ChainInfo",
                               "Get basic information of CITA service running on the node, value is economic model;",
                               ["NodeIP", "NodePort", "ChainName", "Operator", "TokenName", "TokenSymbol", "Version"],
                               registry=CITA_Chain)
    Node_Get_NodePeers = Gauge("Node_Get_NodePeers",
                               "Get the number of node connections, value is local connect node conuts;",
                               ["NodeIP", "NodePort"],
                               registry=CITA_Chain)
    Node_Get_ChainNodes = Gauge("Node_Get_ChainNodes",
                                "Get the number of CITA service Consensus nodes, value is node counts by chain;",
                                ["NodeIP", "NodePort"],
                                registry=CITA_Chain)
    Node_Get_LastBlocknumber = Gauge("Node_Get_LastBlocknumber",
                                     "Get the latest block height, value is block number;",
                                     ["NodeIP", "NodePort", "FirstBlocknumberHash", "NodeID", "NodeAddress"],
                                     registry=CITA_Chain)
    Node_CheckProposer = Gauge("Node_CheckProposer",
                                     "CheckProposer, value is 1 or 0;",
                                     ["NodeIP", "NodePort"],
                                     registry=CITA_Chain)
    Node_Get_LastBlocknumberDetails = Gauge("Node_Get_LastBlocknumberDetails",
                                            "Get the hash and timestamp of the last block, value is last block timestamp;",
                                            ["NodeIP", "NodePort", "LastBlocknumber", "LastBlockProposer", "LastBlockHash", "NodeID", "HostPlatform", "HostName", "ConsensusStatus", "SoftVersion"],
                                            registry=CITA_Chain)
    Node_Get_BlockDifference = Gauge("Node_Get_BlockDifference",
                                         "Get current block time and previous block time,label include CurrentHeight, PreviousHeight. value is Calculate the difference into seconds;",
                                         ["NodeIP", "NodePort", "CurrentHeight", "PreviousHeight"],
                                         registry=CITA_Chain)
    Node_Get_DirInfo_TotalFileSize = Gauge("Node_Get_DirInfo_TotalFileSize",
                             "Get TotalFileSize by Node Dir, value is TotalFileSize;",
                                           ["NodeIP", "NodePort", "NodeDir", "NodeDisk"],
                                           registry=CITA_Chain)
    Node_Get_BlockTimeDifference = Gauge("Node_Get_BlockTimeDifference",
                                         "Get current block time and previous block time,value is Calculate the difference into seconds;",
                                         ["NodeIP", "NodePort"],
                                         registry=CITA_Chain)
    Node_Get_LastBlocknumberTransactions = Gauge("Node_Get_LastBlocknumberTransactions",
                                         "Get current block transactions,value is transactions len;",
                                         ["NodeIP", "NodePort"],
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

        if ',' in receive_path:
            path_list = receive_path.split(',')
            for dir_path in path_list:
                GetResult.NodeDir_analysis(dir_path)
                Node_Get_DirInfo_TotalFileSize.labels(NodeIP=NodeIP, NodePort=NodePort, NodeDir=dir_path, NodeDisk=NodeDisk).set(TotalFileSize)
        else:
            dir_path = receive_path
            GetResult.NodeDir_analysis(dir_path)
            Node_Get_DirInfo_TotalFileSize.labels(NodeIP=NodeIP, NodePort=NodePort, NodeDir=dir_path, NodeDisk=NodeDisk).set(TotalFileSize)

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
            ChainNodeList = str(ChainNodesInfo.split('0x')[1])
            ChainNodesCount = (len(ChainNodeList) / 64 - 2)
            Node_Get_ChainNodes.labels(NodeIP=NodeIP, NodePort=NodePort).set(ChainNodesCount)
        Node_Get_LastBlocknumber_by_blockNumber = GetResult.blockNumber()
        if Node_Get_LastBlocknumber_by_blockNumber != -99:
            Blocknumber = Node_Get_LastBlocknumber_by_blockNumber['result']
            Node_Get_LastBlocknumber.labels(
                NodeIP=NodeIP, NodePort=NodePort,
                FirstBlocknumberHash=FirstBlocknumberHash,
                NodeID=node_id, NodeAddress=('0x' + NodeAddress)
            ).set(int(Blocknumber, 16))
        Node_Get_LastBlocknumberDetails_by_getBlockByNumber = GetResult.getBlockByNumber(Blocknumber)
        PreviousBlocknumber = hex(int(Blocknumber,16) - 1)#
        Node_Get_PreviousBlocknumberDetails_by_getBlockByNumber = GetResult.getBlockByNumber(PreviousBlocknumber)
        if Node_Get_LastBlocknumberDetails_by_getBlockByNumber != -99:
            LastBlockHash = Node_Get_LastBlocknumberDetails_by_getBlockByNumber['result']['hash']
            LastBlocknumberTimestamp = Node_Get_LastBlocknumberDetails_by_getBlockByNumber['result']['header']['timestamp']
            LastBlocknumberTransactions = int(len(Node_Get_LastBlocknumberDetails_by_getBlockByNumber['result']['body']['transactions']))#
            LastBlockProposer = Node_Get_LastBlocknumberDetails_by_getBlockByNumber['result']['header']['proposer']
            PreviousBlocknumberTimestamp = Node_Get_PreviousBlocknumberDetails_by_getBlockByNumber['result']['header']['timestamp']#
            TimeDifference = int(LastBlocknumberTimestamp - PreviousBlocknumberTimestamp)#
            m = re.search(NodeAddress,ChainNodeList)
            if m:
                ConsensusStatus = 1
            else:
                ConsensusStatus = 0
            Node_Get_LastBlocknumberDetails.labels(
                NodeIP=NodeIP, NodePort=NodePort,
                LastBlocknumber=int(Blocknumber,16), LastBlockProposer=LastBlockProposer,
                LastBlockHash=LastBlockHash, NodeID=node_id,
                HostPlatform=HostPlatform, HostName=HostName,
                ConsensusStatus=ConsensusStatus,SoftVersion=SoftVersion
            ).set(LastBlocknumberTimestamp)
            Node_Get_BlockDifference.labels(
                NodeIP=NodeIP, NodePort=NodePort,
                CurrentHeight=int(Blocknumber,16),
                PreviousHeight=int(PreviousBlocknumber,16)
            ).set(TimeDifference)
            Node_Get_BlockTimeDifference.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(TimeDifference)
            Node_Get_LastBlocknumberTransactions.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(LastBlocknumberTransactions)
            m = re.search(NodeAddress, LastBlockProposer)
            if m:
                CheckProposer = 1
            else:
                CheckProposer = 0
            Node_CheckProposer.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(CheckProposer)
        Node_Get_NodePeers_by_peerCount = GetResult.peerCount()
        if Node_Get_NodePeers_by_peerCount != -99:
            NodePeers = Node_Get_NodePeers_by_peerCount['result']
            Node_Get_NodePeers.labels(NodeIP=NodeIP, NodePort=NodePort).set(int(NodePeers, 16))

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
