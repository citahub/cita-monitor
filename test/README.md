# Testing

## How to start a local CITA nodes network?

### First of all, prepare cita-node docker image

build base image for cita-node: `$ make build CITA_VERSION=0.24.0`

### To start 1 node

1. generate node config: `$ make config-node`
2. start 1 node: `$ make start-node`
3. query block number: `$ make rpc-block-number`

### To start 4 nodes

1. generate nodes config: `$ make config-nodes`
2. start 4 node: `$ make start-nodes`
3. query block number: `$ make rpc-block-number`

### To start any number of node

1. generate nodes config: `$ make config-nodes NODES_CONFIG=node0:4000,node1:4000,node2:4000,node3:4000,node4:4000`
2. start 5 nodes: `$ make start-nodes NODES="node0 node1 node2 node3 node4"`
3. watch block number: `$ make watch TARGET=rpc-block-number`
4. stop 1 node: `$ make stop-nodes NODES="node3"`
5. watch step 3, block number should be still growing
