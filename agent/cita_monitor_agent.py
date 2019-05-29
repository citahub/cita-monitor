#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This is the agent script for the CITA-Monitor monitoring system.
The data on the chain is obtained by cita-cli and then pulled by prometheus.
"""

# pylint: disable=global-statement, too-many-locals, too-many-branches, too-many-statements, fixme
# TODO: refactor codes to pass pylint

import json
import os
import sys
import time
import platform
import psutil
import prometheus_client
from prometheus_client.core import CollectorRegistry, Gauge
from flask import Response, Flask

# exporter value variable
NODE = sys.argv[1]
NODE_FILE_PATH = sys.argv[3]
NODE_ID = sys.argv[3].split('/')[-1]
SOFT_FILE_PATH = sys.argv[3].rsplit('/', 2)[0]
NODE_FLASK = Flask(__name__)
EXPORTER_PLATFORM = platform.platform()
AGENT_NAME = platform.node()
DISK_TOTAL = None
DISK_USED = None
DISK_FREE = None
ADDRESS = None
FILE_TOTAL_SIZE = None
SOFT_VERSION_TXT = '%s/bin/cita-chain -V' % (SOFT_FILE_PATH)
try:
    SOFT_VERSION_EXEC = os.popen(SOFT_VERSION_TXT)
    SOFT_VERSION = str(SOFT_VERSION_EXEC.read().split(' ')[1].split('\n')[0])
except IndexError:
    SOFT_VERSION = 'null'

# exporter label variable
SERVICE_STATUS_TITLE = "[ value is 1 or 0 ] \
Check the running status of the CITA service, service up is 1 or down is 0."

FIRST_BLOCK_DETAILS_TITLE = "[ value is first block timestamp ] \
Get information about the first block."

CHAIN_INFO_TITLE = "[ value is 1 or 0 ] \
Get the basic information of the chain, the economic model Quota is 0 or Charge is 1."

NODE_PEERS_TITLE = "[ value is local node peer count ] \
Get the number of peers connected to the local node."

CHAIN_NODES_TITLE = "[ value is node count of chain ] \
Get the number of consensus nodes on the chain."

LAST_BLOCK_NUMBER_TITLE = "[ value is last block number ] \
Get the latest block height."

CHECK_PROPOSER_TITLE = "[ value is 1 or 0 ] \
Check the local node address is proposal, proposal is 1 or listeners is 0."

LAST_BLOCK_DETAILS_TITLE = "[ value is last block timestamp ] \
Get the latest block details."

BLOCK_HEIGHT_DIFFERENCE_TITLE = "[ value is interval ] \
Get current block time and previous block time, label include CurrentHeight, PreviousHeight."

NODE_DIR_TOTAL_SIZE_TITLE = "[ value is size ] \
Get the node directory total size."

NODE_DISK_USED_SIZE_TITLE = "[ value is size ] \
Get the disk used size."

NODE_DISK_FREE_SIZE_TITLE = "[ value is size ] \
Get the disk free size."

BLOCK_INTERVAL_TITLE = "[ value is interval ] \
Get current block time and previous block time."

LAST_BLOCK_TRANSACTIONS_TITLE = "[ value is tx counts ] \
Get the number of transactions in the current block."

LAST_BLOCK_QUOTA_USED_TITLE = "[ value is quotaused of block ] \
Get quotaused in current block."

CHAIN_QUOTA_PRICE_TITLE = "[ value is quota price ] \
Get Quota price of chain."

BLOCK_QUOTA_LIMIT_TITLE = "[ value is block quota limit ] \
Get block quota limit of chain."

VOTE_NODE_TITLE = "[ value is confirm vote ] \
Get vote list of current block."

# print exporter info
print("\n----------")
print("monitor node rpc is : ", NODE)
print("node directory is : ", NODE_FILE_PATH)
print("node id is : ", NODE_ID)
print("----------\n")


# class
class ExporterFunctions():
    """This class is to get CITA data"""

    def __init__(self, node_ip, node_port):
        self.node_ip = node_ip
        self.node_port = node_port

    def cli_request(self, payload):
        """Cita-cli request method"""
        req = "timeout 3 cita-cli %s --url http://%s:%s" \
            %(payload, self.node_ip, self.node_port)
        try:
            req_result = os.popen(req).read()
        except OSError:
            log_time = time.asctime(time.localtime(time.time()))
            result = (log_time + " - Error - exec error[ " + req + " ]\n")
        else:
            log_time = time.asctime(time.localtime(time.time()))
            if req_result == '':
                result = (log_time + " - Error - exec timeout[ " + req + " ]\n")
            else:
                result = json.loads(req_result)
        return result

    def quota_price(self):
        """Get CITA quota price via cita-cli"""
        payload = "scm PriceManager getQuotaPrice"
        return self.cli_request(payload)

    def block_limit(self):
        """Get the quota limit for cita blocks with cita-cli"""
        payload = "scm QuotaManager getBQL"
        return self.cli_request(payload)

    def block_number(self):
        """Get the current block height with cita-cli"""
        payload = "rpc blockNumber"
        return self.cli_request(payload)

    def peer_count(self):
        """Get the number of nodes connecting the current node through cita-cli"""
        payload = "rpc peerCount"
        return self.cli_request(payload)

    def block_number_detail(self, block_height):
        """Get detailed information about CITA blocks with cita-cli"""
        payload = "rpc getBlockByNumber --height %s" % (block_height)
        return self.cli_request(payload)

    def metadata(self, block_height):
        """Get metadate with cita-cli"""
        payload = "rpc getMetaData --height %s" % (block_height)
        return self.cli_request(payload)


def dir_analysis(path):
    """Analyze CITA directory size"""
    global DISK_TOTAL, DISK_USED, DISK_FREE, ADDRESS, FILE_TOTAL_SIZE
    get_privkey_txt = "cat %s/privkey" % (path)
    get_privkey_exec = os.popen(get_privkey_txt)
    privkey = str(get_privkey_exec.read())
    get_address_txt = "cita-cli key from-private --private-key %s" % privkey
    get_address_exec = os.popen(get_address_txt)
    get_address_result = json.loads(get_address_exec.read())
    ADDRESS = str(get_address_result['address'])
    disk_usage = psutil.disk_usage(SOFT_FILE_PATH)
    DISK_TOTAL = disk_usage.total
    DISK_USED = disk_usage.used
    DISK_FREE = disk_usage.free
    file_total_size_txt = "cd %s && du | tail -n 1 | awk '{print $1}'" % (path)
    try:
        file_total_size_exec = os.popen(file_total_size_txt)
        FILE_TOTAL_SIZE = file_total_size_exec.read().split('\n')[0]
    except OSError:
        FILE_TOTAL_SIZE = 0


# flask object
@NODE_FLASK.route("/metrics")
def exporter():
    """Agent execution function"""
    # definition tag
    registry = CollectorRegistry(auto_describe=False)
    service_status = Gauge("Node_Get_ServiceStatus",
                           SERVICE_STATUS_TITLE, ["NodeIP", "NodePort"],
                           registry=registry)
    first_block_details = Gauge("Node_Get_FirstBlockNumberDetails",
                                FIRST_BLOCK_DETAILS_TITLE,
                                ["NodeIP", "NodePort", "FirstBlockNumberHash"],
                                registry=registry)
    chain_info = Gauge("Node_Get_ChainInfo",
                       CHAIN_INFO_TITLE, [
                           "NodeIP", "NodePort", "ChainName", "Operator",
                           "TokenName", "TokenSymbol", "Version"
                       ],
                       registry=registry)
    node_peers = Gauge("Node_Get_NodePeers",
                       NODE_PEERS_TITLE, ["NodeIP", "NodePort"],
                       registry=registry)
    chain_nodes = Gauge("Node_Get_ChainNodes",
                        CHAIN_NODES_TITLE, ["NodeIP", "NodePort"],
                        registry=registry)
    last_block_number = Gauge(
        "Node_Get_LastBlockNumber",
        LAST_BLOCK_NUMBER_TITLE,
        ["NodeIP", "NodePort", "FirstBlockNumberHash", "NodeID", "NodeAddress"],
        registry=registry)
    check_proposer = Gauge("Node_CheckProposer",
                           CHECK_PROPOSER_TITLE, ["NodeIP", "NodePort"],
                           registry=registry)
    last_block_details = Gauge(
        "Node_Get_LastBlockNumberDetails",
        LAST_BLOCK_DETAILS_TITLE, [
            "NodeIP", "NodePort", "LastBlocknumber", "LastBlockProposer",
            "LastBlockHash", "NodeID", "HostPlatform", "HostName",
            "ConsensusStatus", "SoftVersion"
        ],
        registry=registry)
    vote_node = Gauge("Node_Get_VoteNode",
                      VOTE_NODE_TITLE,
                      ["NodeIP", "NodePort", "NodeID", "Voter"],
                      registry=registry)
    block_height_difference = Gauge(
        "Node_Get_BlockDifference",
        BLOCK_HEIGHT_DIFFERENCE_TITLE,
        ["NodeIP", "NodePort", "CurrentHeight", "PreviousHeight"],
        registry=registry)
    dir_total_size = Gauge("Node_Get_DirInfo_TotalFileSize",
                           NODE_DIR_TOTAL_SIZE_TITLE,
                           ["NodeIP", "NodePort", "NodeDir"],
                           registry=registry)
    disk_used_size = Gauge("Node_Get_DiskInfo_UsedSize",
                           NODE_DISK_USED_SIZE_TITLE,
                           ["NodeIP", "NodePort", "NodeDir"],
                           registry=registry)
    disk_free_size = Gauge("Node_Get_DiskInfo_FreeSize",
                           NODE_DISK_FREE_SIZE_TITLE,
                           ["NodeIP", "NodePort", "NodeDir"],
                           registry=registry)
    block_interval = Gauge("Node_Get_BlockTimeDifference",
                           BLOCK_INTERVAL_TITLE, ["NodeIP", "NodePort"],
                           registry=registry)
    last_block_transactions = Gauge("Node_Get_LastBlockNumberTransactions",
                                    LAST_BLOCK_TRANSACTIONS_TITLE,
                                    ["NodeIP", "NodePort"],
                                    registry=registry)
    last_block_quota_used = Gauge("Node_Get_LastBlockNumberQuotaUsed",
                                  LAST_BLOCK_QUOTA_USED_TITLE,
                                  ["NodeIP", "NodePort"],
                                  registry=registry)
    chain_quota_price = Gauge("Node_Get_QuotaPrice",
                              CHAIN_QUOTA_PRICE_TITLE, ["NodeIP", "NodePort"],
                              registry=registry)
    block_quota_limit = Gauge("Node_Get_BlockQuotaLimit",
                              BLOCK_QUOTA_LIMIT_TITLE, ["NodeIP", "NodePort"],
                              registry=registry)

    # run exporter
    node_ip = str(NODE.split(':')[0])
    node_port = str(NODE.split(':')[1])
    check_process = os.popen("ps alx |grep 'cita-chain' |grep -c -v grep")
    if check_process.read() == '0\n':
        service_status.labels(NodeIP=node_ip, NodePort=node_port).set(0)
        return Response(prometheus_client.generate_latest(registry),
                        mimetype="text/plain")

    service_status.labels(NodeIP=node_ip, NodePort=node_port).set(1)
    class_result = ExporterFunctions(node_ip, node_port)
    dir_analysis(NODE_FILE_PATH)
    dir_total_size.labels(
        NodeIP=node_ip,
        NodePort=node_port,
        NodeDir=NODE_FILE_PATH,
    ).set(FILE_TOTAL_SIZE)
    disk_used_size.labels(
        NodeIP=node_ip,
        NodePort=node_port,
        NodeDir=NODE_FILE_PATH,
    ).set(DISK_USED)
    disk_free_size.labels(
        NodeIP=node_ip,
        NodePort=node_port,
        NodeDir=NODE_FILE_PATH,
    ).set(DISK_FREE)

    first_block_info = class_result.block_number_detail('0x0')
    if 'result' in first_block_info:
        first_block_hash = first_block_info['result']['hash']
        first_block_time = first_block_info['result']['header']['timestamp']
        first_block_details.labels(
            NodeIP=node_ip,
            NodePort=node_port,
            FirstBlockNumberHash=first_block_hash).set(first_block_time)
    else:
        print(first_block_info)
    block_number_info = class_result.block_number()
    if 'result' in block_number_info:
        hex_number = block_number_info['result']
        previous_hex_number = hex(int(hex_number, 16) - 1)
        last_block_number.labels(NodeIP=node_ip,
                                 NodePort=node_port,
                                 FirstBlockNumberHash=first_block_hash,
                                 NodeID=NODE_ID,
                                 NodeAddress=ADDRESS).set(int(hex_number, 16))
    else:
        print(block_number_info)
    metadata_info = class_result.metadata(hex_number)
    if 'result' in metadata_info:
        chain_name = metadata_info['result']['chainName']
        operator = metadata_info['result']['operator']
        token_name = metadata_info['result']['tokenName']
        token_symbol = metadata_info['result']['tokenSymbol']
        economical_model = metadata_info['result']['economicalModel']
        chain_version = metadata_info['result']['version']
        chain_info.labels(NodeIP=node_ip,
                          NodePort=node_port,
                          ChainName=chain_name,
                          Operator=operator,
                          TokenName=token_name,
                          TokenSymbol=token_symbol,
                          Version=chain_version).set(economical_model)
        consensus_node_list = metadata_info['result']['validators']
        consensus_node_count = len(consensus_node_list)
        chain_nodes.labels(NodeIP=node_ip,
                           NodePort=node_port).set(consensus_node_count)
    else:
        print(metadata_info)
    block_info = class_result.block_number_detail(hex_number)
    previous_block_info = class_result.block_number_detail(previous_hex_number)
    if 'result' in block_info and 'result' in previous_block_info:
        block_head_info = block_info['result']['header']
        if block_head_info.get('quotaUsed'):
            block_quota_used = int(block_head_info['quotaUsed'], 16)
        else:
            #Get the previous version of CITA v0.19.1 gasUsed
            block_head_info.get('gasUsed')
            block_quota_used = int(block_head_info['gasUsed'], 16)
        block_commits = list(
            block_info['result']['header']['proof']['Bft']['commits'].keys())
        consensus_nodes_count = len(consensus_node_list)
        for i in range(consensus_nodes_count):
            voter = consensus_node_list[i]
            if voter in block_commits:
                vote_status = 1
            else:
                vote_status = 0
            vote_node.labels(NodeIP=node_ip,
                             NodePort=node_port,
                             NodeID=NODE_ID,
                             Voter=voter).set(vote_status)
        block_hash = block_info['result']['hash']
        block_time = int(block_head_info['timestamp'])
        block_transactions = int(
            len(block_info['result']['body']['transactions']))
        block_proposer = block_head_info['proposer']
        previous_block_time = int(
            previous_block_info['result']['header']['timestamp'])
        interval = abs(block_time - previous_block_time)
        if ADDRESS in consensus_node_list:
            consensus = 1
        else:
            consensus = 0
        last_block_details.labels(NodeIP=node_ip,
                                  NodePort=node_port,
                                  LastBlocknumber=int(hex_number, 16),
                                  LastBlockProposer=block_proposer,
                                  LastBlockHash=block_hash,
                                  NodeID=NODE_ID,
                                  HostPlatform=EXPORTER_PLATFORM,
                                  HostName=AGENT_NAME,
                                  ConsensusStatus=consensus,
                                  SoftVersion=SOFT_VERSION).set(block_time)
        block_height_difference.labels(NodeIP=node_ip,
                                       NodePort=node_port,
                                       CurrentHeight=int(hex_number, 16),
                                       PreviousHeight=int(
                                           previous_hex_number,
                                           16)).set(interval)
        block_interval.labels(NodeIP=node_ip, NodePort=node_port).set(interval)
        last_block_transactions.labels(
            NodeIP=node_ip, NodePort=node_port).set(block_transactions)
        last_block_quota_used.labels(NodeIP=node_ip,
                                     NodePort=node_port).set(block_quota_used)
        if ADDRESS == block_proposer:
            proposer = 1
        else:
            proposer = 0
        check_proposer.labels(NodeIP=node_ip, NodePort=node_port).set(proposer)
    else:
        print(block_info)
        print(previous_block_info)
    peer_info = class_result.peer_count()
    if 'result' in peer_info:
        peers = peer_info['result']
        node_peers.labels(NodeIP=node_ip,
                          NodePort=node_port).set(int(peers, 16))
    else:
        print(peer_info)
    quota_price = class_result.quota_price()
    if 'result' in quota_price:
        price = quota_price['result']
        chain_quota_price.labels(NodeIP=node_ip,
                                 NodePort=node_port).set(int(price, 16))
    else:
        print(quota_price)
    block_limit = class_result.block_limit()
    if 'result' in block_limit:
        limit = block_limit['result']
        block_quota_limit.labels(NodeIP=node_ip,
                                 NodePort=node_port).set(int(limit, 16))
    else:
        print(block_limit)

    return Response(prometheus_client.generate_latest(registry),
                    mimetype="text/plain")


# flask object
@NODE_FLASK.route("/")
def index():
    """Page data view entry"""
    index_html = "<h2>访问 /metrics 路径获取数据采集信息</h2>"
    return index_html


# main
if __name__ == "__main__":
    NODE_FLASK.run(host="0.0.0.0", port=int(sys.argv[2]))
