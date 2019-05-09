#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
import prometheus_client
from prometheus_client import Counter, Enum, Gauge
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
node_file_path = sys.argv[3]
node_id = sys.argv[3].split('/')[-1]
soft_file_path = sys.argv[3].rsplit('/', 2)[0]
# 创建 flask 进程
node_flask = Flask(__name__)
# 获取主机操作系统平台
host_os = platform.platform()
# 获取 agent 主机名
agent_name = platform.node()
# 获取 CITA 运行软件版本号
soft_version_txt = '%s/bin/cita-chain -V' % (soft_file_path)
try:
    soft_version_exec = os.popen(soft_version_txt)
    soft_version = str(soft_version_exec.read().split(' ')[1].split('\n')[0])
except:
    soft_version = 'null'
print("node is : ", node)
print("node directory is : ", node_file_path)
print("node id is : ", node_id)


# 定义 cita-cli 请求功能类
class MonitorFunction(object):
    # 定义初始化变量
    def __init__(self, node_ip, node_port):
        self.node_ip = node_ip
        self.node_port = node_port

    #
    def cli_request(self, payload):
        r = "timeout 3 cita-cli %s --url http://%s:%s" % (payload, self.node_ip,
                                                          self.node_port)
        print(r)
        try:
            req_result = os.popen(r).read()
        except:
            return -99
        else:
            if req_result == '':
                exit()
            else:
                result = json.loads(req_result)
                return result

    #
    def quota_price(self):
        payload = "scm PriceManager getQuotaPrice"
        return self.cli_request(payload)

    #
    def block_limit(self):
        payload = "scm QuotaManager getBQL"
        return self.cli_request(payload)

    #
    def block_number(self):
        payload = "rpc blockNumber"
        return self.cli_request(payload)

    #
    def peer_count(self):
        payload = "rpc peerCount"
        return self.cli_request(payload)

    #
    def block_number_detail(self, Height):
        payload = "rpc getBlockByNumber --height %s" % (Height)
        return self.cli_request(payload)

    #
    def metadata(self):
        payload = "rpc getMetaData"
        return self.cli_request(payload)

    #
    def dir_analysis(self, path):
        # 返回全局变量
        global disk_total
        global address
        global file_size_total

        privkey_txt = "cat %s/privkey" % (path)
        privkey_exec = os.popen(privkey_txt)
        privkey = str(privkey_exec.read())
        address_txt = "cita-cli key from-private --private-key %s" % privkey
        address_exec = os.popen(address_txt)
        address_result = json.loads(address_exec.read())
        address = str(address_result['address'])
        disk_total = psutil.disk_usage(soft_file_path).total
        file_size_total_txt = "cd %s && du | tail -n 1 | awk '{print $1}'" % (
            path)
        try:
            file_size_total_exec = os.popen(file_size_total_txt)
            file_size_total = file_size_total_exec.read().split('\n')[0]
        except:
            file_size_total = 0


# flask 对象
@node_flask.route("/metrics")
def GetLabels():
    # 定义 prometheus 标签
    registry = CollectorRegistry(auto_describe=False)
    #
    Node_Get_ServiceStatus = Gauge(
        "Node_Get_ServiceStatus",
        "Check local running cita services, value return 1 when running; return 0 is not running;",
        ["NodeIP", "NodePort"],
        registry=registry)
    #
    Node_Get_FirstBlockNumberDetails = Gauge(
        "Node_Get_FirstBlockNumberDetails",
        "Get the hash and timestamp of the first block, value is timestamp;",
        ["NodeIP", "NodePort", "FirstBlockNumberHash"],
        registry=registry)
    #
    Node_Get_ChainInfo = Gauge(
        "Node_Get_ChainInfo",
        "Get basic information of CITA service running on the node, value is economic model;",
        [
            "NodeIP", "NodePort", "ChainName", "Operator", "TokenName",
            "TokenSymbol", "Version"
        ],
        registry=registry)
    #
    Node_Get_NodePeers = Gauge(
        "Node_Get_NodePeers",
        "Get the number of node connections, value is local connect node conuts;",
        ["NodeIP", "NodePort"],
        registry=registry)
    #
    Node_Get_ChainNodes = Gauge(
        "Node_Get_ChainNodes",
        "Get the number of CITA service Consensus nodes, value is node counts by chain;",
        ["NodeIP", "NodePort"],
        registry=registry)
    #
    Node_Get_LastBlockNumber = Gauge(
        "Node_Get_LastBlockNumber",
        "Get the latest block height, value is block number;",
        ["NodeIP", "NodePort", "FirstBlockNumberHash", "NodeID", "NodeAddress"],
        registry=registry)
    #
    Node_CheckProposer = Gauge("Node_CheckProposer",
                               "check proposer, value is 1 or 0;",
                               ["NodeIP", "NodePort"],
                               registry=registry)
    #
    Node_Get_LastBlockNumberDetails = Gauge(
        "Node_Get_LastBlockNumberDetails",
        "Get the hash and timestamp of the last block, value is last block timestamp;",
        [
            "NodeIP", "NodePort", "LastBlocknumber", "LastBlockProposer",
            "LastBlockHash", "NodeID", "HostPlatform", "HostName",
            "ConsensusStatus", "SoftVersion"
        ],
        registry=registry)
    #
    Node_Get_BlockDifference = Gauge(
        "Node_Get_BlockDifference",
        "Get current block time and previous block time,label include CurrentHeight, PreviousHeight. value is Calculate the difference into seconds;",
        ["NodeIP", "NodePort", "CurrentHeight", "PreviousHeight"],
        registry=registry)
    #
    Node_Get_DirInfo_TotalFileSize = Gauge(
        "Node_Get_DirInfo_TotalFileSize",
        "Get TotalFileSize by Node Dir, value is TotalFileSize;",
        ["NodeIP", "NodePort", "NodeDir", "NodeDisk"],
        registry=registry)
    #
    Node_Get_BlockTimeDifference = Gauge(
        "Node_Get_BlockTimeDifference",
        "Get current block time and previous block time,value is Calculate the difference into seconds;",
        ["NodeIP", "NodePort"],
        registry=registry)
    #
    Node_Get_LastBlockNumberTransactions = Gauge(
        "Node_Get_LastBlockNumberTransactions",
        "Get current block transactions,value is transactions len;",
        ["NodeIP", "NodePort"],
        registry=registry)
    #
    Node_Get_LastBlockNumberQuotaUsed = Gauge(
        "Node_Get_LastBlockNumberQuotaUsed",
        "Get current block quotaused,value is quotaused count;",
        ["NodeIP", "NodePort"],
        registry=registry)
    #
    Node_Get_QuotaPrice = Gauge("Node_Get_QuotaPrice",
                                "Get Quota price of current chain;",
                                ["NodeIP", "NodePort"],
                                registry=registry)
    #
    Node_Get_BlockQuotaLimit = Gauge("Node_Get_BlockQuotaLimit",
                                     "Get block quota limit of current chain;",
                                     ["NodeIP", "NodePort"],
                                     registry=registry)
    #---
    # 切割 node 信息
    node_ip = str(node.split(':')[0])
    node_port = str(node.split(':')[1])
    # 检查本地是否存在 CITA 服务进程
    check_process = os.popen("ps alx |grep 'cita-chain' |grep -c -v grep")
    if check_process.read() == '0\n':
        Node_Get_ServiceStatus.labels(NodeIP=node_ip, NodePort=node_port).set(0)
        return Response(prometheus_client.generate_latest(registry),
                        mimetype="text/plain")
    # 执行 prometheus 标签功能请求
    else:
        Node_Get_ServiceStatus.labels(NodeIP=node_ip, NodePort=node_port).set(1)
        class_result = MonitorFunction(node_ip, node_port)
        # 获取目录容量
        if ',' in node_file_path:
            path_list = node_file_path.split(',')
            for path in path_list:
                class_result.dir_analysis(path)
                Node_Get_DirInfo_TotalFileSize.labels(
                    NodeIP=node_ip,
                    NodePort=node_port,
                    NodeDir=path,
                    NodeDisk=disk_total).set(file_size_total)
        else:
            path = node_file_path
            class_result.dir_analysis(path)
            Node_Get_DirInfo_TotalFileSize.labels(
                NodeIP=node_ip,
                NodePort=node_port,
                NodeDir=path,
                NodeDisk=disk_total).set(file_size_total)
        # 获取创世块信息
        first_block_info = class_result.block_number_detail('0x0')
        if first_block_info != -99:
            first_block_hash = first_block_info['result']['hash']
            first_block_time = first_block_info['result']['header']['timestamp']
            Node_Get_FirstBlockNumberDetails.labels(
                NodeIP=node_ip,
                NodePort=node_port,
                FirstBlockNumberHash=first_block_hash).set(first_block_time)
        # 获取链信息
        metadata_info = class_result.metadata()
        if metadata_info != -99:
            chain_name = metadata_info['result']['chainName']
            operator = metadata_info['result']['operator']
            token_name = metadata_info['result']['tokenName']
            token_symbol = metadata_info['result']['tokenSymbol']
            economical_model = metadata_info['result']['economicalModel']
            chain_version = metadata_info['result']['version']
            Node_Get_ChainInfo.labels(
                NodeIP=node_ip,
                NodePort=node_port,
                ChainName=chain_name,
                Operator=operator,
                TokenName=token_name,
                TokenSymbol=token_symbol,
                Version=chain_version).set(economical_model)
            consensus_node_list = metadata_info['result']['validators']
            consensus_node_count = len(consensus_node_list)
            Node_Get_ChainNodes.labels(
                NodeIP=node_ip, NodePort=node_port).set(consensus_node_count)
        # 获取最新区块高度
        block_number_info = class_result.block_number()
        if block_number_info != -99:
            hex_number = block_number_info['result']
            # 获取上一个区块高度
            previous_hex_number = hex(int(hex_number, 16) - 1)
            Node_Get_LastBlockNumber.labels(
                NodeIP=node_ip,
                NodePort=node_port,
                FirstBlockNumberHash=first_block_hash,
                NodeID=node_id,
                NodeAddress=address).set(int(hex_number, 16))
        # 获取最新区块详细信息
        block_info = class_result.block_number_detail(hex_number)
        previous_block_info = class_result.block_number_detail(
            previous_hex_number)
        if block_info != -99 and previous_block_info != -99:
            block_head_info = block_info['result']['header']
            if block_head_info.get('quotaUsed'):
                block_quota_used = int(block_head_info['quotaUsed'], 16)
            else:
                #Get the previous version of CITA v0.19.1 gasUsed
                block_head_info.get('gasUsed')
                block_quota_used = int(block_head_info['gasUsed'], 16)
            block_hash = block_info['result']['hash']
            block_time = int(block_head_info['timestamp'])
            block_transactions = int(
                len(block_info['result']['body']['transactions']))
            block_proposer = block_head_info['proposer']
            previous_block_time = int(
                previous_block_info['result']['header']['timestamp'])
            interval = abs(block_time - previous_block_time)
            #
            if address in consensus_node_list:
                consensus = 1
            else:
                consensus = 0
            #
            Node_Get_LastBlockNumberDetails.labels(
                NodeIP=node_ip,
                NodePort=node_port,
                LastBlocknumber=int(hex_number, 16),
                LastBlockProposer=block_proposer,
                LastBlockHash=block_hash,
                NodeID=node_id,
                HostPlatform=host_os,
                HostName=agent_name,
                ConsensusStatus=consensus,
                SoftVersion=soft_version).set(block_time)
            #
            Node_Get_BlockDifference.labels(NodeIP=node_ip,
                                            NodePort=node_port,
                                            CurrentHeight=int(hex_number, 16),
                                            PreviousHeight=int(
                                                previous_hex_number,
                                                16)).set(interval)
            #
            Node_Get_BlockTimeDifference.labels(
                NodeIP=node_ip, NodePort=node_port).set(interval)
            #
            Node_Get_LastBlockNumberTransactions.labels(
                NodeIP=node_ip, NodePort=node_port).set(block_transactions)
            #
            Node_Get_LastBlockNumberQuotaUsed.labels(
                NodeIP=node_ip, NodePort=node_port).set(block_quota_used)
            #
            if address == block_proposer:
                proposer = 1
            else:
                proposer = 0
            #
            Node_CheckProposer.labels(NodeIP=node_ip,
                                      NodePort=node_port).set(proposer)
        # 获取节点的 peer 数量
        peer_info = class_result.peer_count()
        if peer_info != -99:
            peers = peer_info['result']
            Node_Get_NodePeers.labels(NodeIP=node_ip,
                                      NodePort=node_port).set(int(peers, 16))
        # 获取链上的 quota price
        quota_price = class_result.quota_price()
        if quota_price != -99:
            price = quota_price['result']
            Node_Get_QuotaPrice.labels(NodeIP=node_ip,
                                       NodePort=node_port).set(int(price, 16))
        # 获取链上的单个 block quota limit
        block_limit = class_result.block_limit()
        if block_limit != -99:
            limit = block_limit['result']
            Node_Get_BlockQuotaLimit.labels(NodeIP=node_ip,
                                            NodePort=node_port).set(
                                                int(limit, 16))
    # 返回标签数据
    return Response(prometheus_client.generate_latest(registry),
                    mimetype="text/plain")


# flask 对象
@node_flask.route("/")
def Root():
    index = "<h2>访问 /metrics 路径获取数据采集信息</h2>"
    return index


# Run
if __name__ == "__main__":
    #运行 flask 进程
    node_flask.run(host="0.0.0.0", port=int(sys.argv[2]))
