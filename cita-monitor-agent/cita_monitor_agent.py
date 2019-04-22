#!/usr/bin/python3
# -*- coding: utf-8 -*-
# 普通变量小写开头驼峰格式
# 重要变量大写开头驼峰格式
# Prometheus 标签大写开头+下划线格式
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

# 接收变量传递
node = sys.argv[1]
receivePath = sys.argv[3]
nodeId = sys.argv[4]
softPath = sys.argv[5]
diskPath = sys.argv[6]
# 创建 flask 进程
nodeFlask = Flask(__name__)
# 获取主机操作系统平台
hostPlatform = platform.platform()
# 获取主机名
hostName = platform.node()
# 获取 CITA 运行软件版本号
getSoftVersionTxt = '%s/bin/cita-chain -V' %(softPath)
try:
    getsoftVersionExec = os.popen(getSoftVersionTxt)
    softVersion = str(getsoftVersionExec.read().split(' ')[1].split('\n')[0])
except:
    softVersion = 'null'

# 定义 cita-cli 请求功能类
class Monitor_Function(object):
    # 定义初始化变量
    def __init__(self, NodeIP, NodePort):
        self.NodeIP = NodeIP
        self.NodePort = NodePort
    #
    def citaCliRequest(self, payload):
        r = "timeout 3 cita-cli %s --url http://%s:%s" %(payload,self.NodeIP,self.NodePort)
        try:
            rResult = os.popen(r).read()
        except:
            return -99
        else:
            if rResult == '':
                print(r)
                exit()
            else:
                payloadResult = json.loads(rResult)
                return payloadResult
    #
    def getQuotaPrice(self):
        payload = "scm PriceManager getQuotaPrice"
        return self.citaCliRequest(payload)
    #
    def getBlockLimit(self):
        payload = "scm QuotaManager getBQL"
        return self.citaCliRequest(payload)
    #
    def blockNumber(self):
        payload = "rpc blockNumber"
        return self.citaCliRequest(payload)
    #
    def peerCount(self):
        payload = "rpc peerCount"
        return self.citaCliRequest(payload)
    #
    def getBlockByNumber(self,Height):
        payload = "rpc getBlockByNumber --height %s" %(Height)
        return self.citaCliRequest(payload)
    #
    def getMetaData(self):
        payload = "rpc getMetaData"
        return self.citaCliRequest(payload)
    #
    def nodeManagerListNode(self):
        payload = "scm NodeManager listNode"
        return self.citaCliRequest(payload)
    #
    def nodeDirAnalysis(self, dirPath):
        # 返回全局变量
        global TotalFileSize
        global NodeAddress
        global NodeDisk
        privkey = "cat %s/privkey" %(dirPath)
        privkeyResult = os.popen(privkey)
        nodePrivkey = str(privkeyResult.read())
        NodeAddress = "cita-cli key from-private --private-key %s" % nodePrivkey
        f = os.popen(NodeAddress)
        addressInfo = json.loads(f.read())
        NodeAddress = addressInfo['address']
        NodeAddress = str(NodeAddress.split('0x')[1].split('\n')[0])
        NodeDisk = psutil.disk_usage(diskPath).total
        totalFileSizeTxt = "cd %s && du | tail -n 1 | awk '{print $1}'" %(dirPath)
        try:
            totalFileSizeExec = os.popen(totalFileSizeTxt)
            TotalFileSize = totalFileSizeExec.read().split('\n')[0]
        except:
            TotalFileSize = 0

# flask 对象
@nodeFlask.route("/metrics")
def Node_Get():
    # 定义 prometheus 标签
    CITARegistry = CollectorRegistry(auto_describe=False)
    #
    Node_Get_ServiceStatus = Gauge(
        "Node_Get_ServiceStatus",
        "Check local running cita services, value return 1 when running; return 0 is not running;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
    #
    Node_Get_FirstBlocknumberDetails = Gauge(
        "Node_Get_FirstBlocknumberDetails",
        "Get the hash and timestamp of the first block, value is timestamp;",
        ["NodeIP", "NodePort", "FirstBlockNumberHash"],
        registry=CITARegistry
    )
    #
    Node_Get_ChainInfo = Gauge(
        "Node_Get_ChainInfo",
        "Get basic information of CITA service running on the node, value is economic model;",
        ["NodeIP", "NodePort", "ChainName", "Operator", "TokenName", "TokenSymbol", "Version"],
        registry=CITARegistry
    )
    #
    Node_Get_NodePeers = Gauge(
        "Node_Get_NodePeers",
        "Get the number of node connections, value is local connect node conuts;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
    #
    Node_Get_ChainNodes = Gauge(
        "Node_Get_ChainNodes",
        "Get the number of CITA service Consensus nodes, value is node counts by chain;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
    #
    Node_Get_LastBlocknumber = Gauge(
        "Node_Get_LastBlocknumber",
        "Get the latest block height, value is block number;",
        ["NodeIP", "NodePort", "FirstBlockNumberHash", "NodeID", "NodeAddress"],
        registry=CITARegistry
    )
    #
    Node_checkProposer = Gauge(
        "Node_checkProposer",
        "checkProposer, value is 1 or 0;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
    #
    Node_Get_LastBlocknumberDetails = Gauge(
        "Node_Get_LastBlocknumberDetails",
        "Get the hash and timestamp of the last block, value is last block timestamp;",
        [
            "NodeIP", "NodePort", "LastBlocknumber", "LastBlockProposer",
            "LastBlockHash", "NodeID", "HostPlatform", "HostName",
            "ConsensusStatus", "SoftVersion"
        ],
        registry=CITARegistry
    )
    #
    Node_Get_BlockDifference = Gauge(
        "Node_Get_BlockDifference",
        "Get current block time and previous block time,label include CurrentHeight, PreviousHeight. value is Calculate the difference into seconds;",
        ["NodeIP", "NodePort", "CurrentHeight", "PreviousHeight"],
        registry=CITARegistry
    )
    #
    Node_Get_DirInfo_TotalFileSize = Gauge(
        "Node_Get_DirInfo_TotalFileSize",
        "Get TotalFileSize by Node Dir, value is TotalFileSize;",
        ["NodeIP", "NodePort", "NodeDir", "NodeDisk"],
        registry=CITARegistry
    )
    #
    Node_Get_BlocktimeDifference = Gauge(
        "Node_Get_BlocktimeDifference",
        "Get current block time and previous block time,value is Calculate the difference into seconds;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
    #
    Node_Get_lastBlockNumberTransactions = Gauge(
        "Node_Get_lastBlockNumberTransactions",
        "Get current block transactions,value is transactions len;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
    #
    Node_Get_LastBlocknumberQuotaUsed = Gauge(
        "Node_Get_LastBlocknumberQuotaUsed",
        "Get current block quotaused,value is quotaused count;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
    #
    Node_Get_QuotaPrice = Gauge(
        "Node_Get_QuotaPrice",
        "Get Quota price of current chain;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
    #
    Node_Get_BlockQuotaLimit = Gauge(
        "Node_Get_BlockQuotaLimit",
        "Get block quota limit of current chain;",
        ["NodeIP", "NodePort"],
        registry=CITARegistry
    )
#---
    # 切割 node 信息
    NodeIP = str(node.split(':')[0])
    NodePort = str(node.split(':')[1])
    # 检查本地是否存在 CITA 服务进程
    checkCitaProcess = os.popen("ps alx |grep 'cita-chain' |grep -c -v grep")
    if checkCitaProcess.read() == '0\n':
        Node_Get_ServiceStatus.labels(NodeIP=NodeIP,NodePort=NodePort).set(0)
        return Response(prometheus_client.generate_latest(CITARegistry), mimetype="text/plain")
    # 执行 prometheus 标签功能请求
    else:
        Node_Get_ServiceStatus.labels(NodeIP=NodeIP, NodePort=NodePort).set(1)
        getResult = Monitor_Function(NodeIP, NodePort)
        # 获取目录容量
        if ',' in receivePath:
            pathList = receivePath.split(',')
            for dirPath in pathList:
                getResult.nodeDirAnalysis(dirPath)
                Node_Get_DirInfo_TotalFileSize.labels(
                    NodeIP=NodeIP, NodePort=NodePort,
                    NodeDir=dirPath, NodeDisk=NodeDisk
                ).set(TotalFileSize)
        else:
            dirPath = receivePath
            getResult.nodeDirAnalysis(dirPath)
            Node_Get_DirInfo_TotalFileSize.labels(
                NodeIP=NodeIP, NodePort=NodePort,
                NodeDir=dirPath, NodeDisk=NodeDisk
            ).set(TotalFileSize)
        # 获取创世块信息
        fncGetBlockByNumber = getResult.getBlockByNumber('0x0')
        if fncGetBlockByNumber != -99:
            firstBlockNumberHash = fncGetBlockByNumber['result']['hash']
            firstBlockNumberTimestamp = fncGetBlockByNumber['result']['header']['timestamp']
            Node_Get_FirstBlocknumberDetails.labels(
                NodeIP=NodeIP, NodePort=NodePort,FirstBlockNumberHash=firstBlockNumberHash
            ).set(firstBlockNumberTimestamp)
        # 获取链信息
        fncGetMetaData = getResult.getMetaData()
        if fncGetMetaData != -99:
            chainName = fncGetMetaData['result']['chainName']
            chainOperator = fncGetMetaData['result']['operator']
            chainTokenName = fncGetMetaData['result']['tokenName']
            chainTokenSymbol = fncGetMetaData['result']['tokenSymbol']
            chainEconomicalModel = fncGetMetaData['result']['economicalModel']
            chainVersion = fncGetMetaData['result']['version']
            Node_Get_ChainInfo.labels(
                NodeIP=NodeIP, NodePort=NodePort, ChainName=chainName,
                Operator=chainOperator, TokenName=chainTokenName,
                TokenSymbol=chainTokenSymbol, Version=chainVersion
            ).set(chainEconomicalModel)
        # 获取链上节点列表
        fncNodeManagerListNode = getResult.nodeManagerListNode()
        if fncNodeManagerListNode != -99:
            chainNodesInfo = fncNodeManagerListNode['result']
            chainNodeList = str(chainNodesInfo.split('0x')[1])
            chainNodesCount = (len(chainNodeList) / 64 - 2)
            Node_Get_ChainNodes.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(chainNodesCount)
        # 获取最新区块高度
        fncBlockNumber = getResult.blockNumber()
        if fncBlockNumber != -99:
            blockNumber = fncBlockNumber['result']
            # 获取上一个区块高度
            previousBlockNumber = hex(int(blockNumber,16) - 1)
            Node_Get_LastBlocknumber.labels(
                NodeIP=NodeIP, NodePort=NodePort,
                FirstBlockNumberHash=firstBlockNumberHash,
                NodeID=nodeId, NodeAddress=('0x' + NodeAddress)
            ).set(int(blockNumber, 16))
        # 获取最新区块详细信息
        fncGetBlockByNumber = getResult.getBlockByNumber(blockNumber)
        fncGetBlockByNumber_previous = getResult.getBlockByNumber(previousBlockNumber)
        if fncGetBlockByNumber != -99 and fncGetBlockByNumber_previous != -99:
            lastBlockQuotaUsed = int(fncGetBlockByNumber['result']['header']['quotaUsed'],16)
            lastBlockHash = fncGetBlockByNumber['result']['hash']
            lastBlockNumberTimestamp = fncGetBlockByNumber['result']['header']['timestamp']
            lastBlockNumberTransactions = int(len(fncGetBlockByNumber['result']['body']['transactions']))
            lastBlockProposer = fncGetBlockByNumber['result']['header']['proposer']
            previousBlockNumberTimestamp = fncGetBlockByNumber_previous['result']['header']['timestamp']
            timeDifference = int(lastBlockNumberTimestamp - previousBlockNumberTimestamp)
            #
            match = re.search(NodeAddress,chainNodeList)
            if match:
                consensusStatus = 1
            else:
                consensusStatus = 0
            #
            Node_Get_LastBlocknumberDetails.labels(
                NodeIP=NodeIP, NodePort=NodePort,
                LastBlocknumber=int(blockNumber,16), LastBlockProposer=lastBlockProposer,
                LastBlockHash=lastBlockHash, NodeID=nodeId,
                HostPlatform=hostPlatform, HostName=hostName,
                ConsensusStatus=consensusStatus,SoftVersion=softVersion
            ).set(lastBlockNumberTimestamp)
            #
            Node_Get_BlockDifference.labels(
                NodeIP=NodeIP, NodePort=NodePort,
                CurrentHeight=int(blockNumber,16),
                PreviousHeight=int(previousBlockNumber,16)
            ).set(timeDifference)
            #
            Node_Get_BlocktimeDifference.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(timeDifference)
            #
            Node_Get_lastBlockNumberTransactions.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(lastBlockNumberTransactions)
            #
            Node_Get_LastBlocknumberQuotaUsed.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(lastBlockQuotaUsed)
            #
            match = re.search(NodeAddress, lastBlockProposer)
            if match:
                checkProposer = 1
            else:
                checkProposer = 0
            #
            Node_checkProposer.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(checkProposer)
        # 获取节点的 peer 数量
        fncPeerCount = getResult.peerCount()
        if fncPeerCount != -99:
            nodePeers = fncPeerCount['result']
            Node_Get_NodePeers.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(int(nodePeers, 16))
        # 获取链上的 quota price
        fncGetQuotaPrice =  getResult.getQuotaPrice()
        if fncGetQuotaPrice != -99:
            quotaPrice = fncGetQuotaPrice['result']
            Node_Get_QuotaPrice.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(int(quotaPrice, 16))
        # 获取链上的单个 block quota limit
        fncGetBlockLimit = getResult.getBlockLimit()
        if fncGetBlockLimit != -99:
            blockQuotaLimit = fncGetBlockLimit['result']
            Node_Get_BlockQuotaLimit.labels(
                NodeIP=NodeIP, NodePort=NodePort
            ).set(int(blockQuotaLimit, 16))
    # 返回标签数据
    return Response(prometheus_client.generate_latest(CITARegistry), mimetype="text/plain")

# flask 对象
@nodeFlask.route("/")
def index():
    NodeIP = str(node.split(':')[0])
    NodePort = str(node.split(':')[1])
    indexText = "<h2>访问 Metrics 路径获取数据采集信息<br><br><a href='http://" + NodeIP + ':' + sys.argv[2] + "/metrics'>点击跳转 Metrics</a></h2>"
    return indexText

# Run
if __name__ == "__main__":
    #运行 flask 进程
    nodeFlask.run(host="0.0.0.0", port=int(sys.argv[2]))