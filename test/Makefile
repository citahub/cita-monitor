.DEFAULT_GOAL:=help
SHELL = /bin/sh

# main receipts
.PHONY: deps build clean help
# receipts for Code Quality
.PHONY: code-quality lint-shell-code format-shell-code
# receipts for Testing
.PHONY: test test-unit test-intergration

.SILENT: help

# DEFINE GLOBAL VARIABLES
RPC_CALL_COUNT=0 # counter for cita_rpc, so that each "id" in RPC request params is unqiue 

# DEFINE FUNCTIONS

# usage: $(call cita_rpc,host:port,method,params)
# e.g.: $(call cita_rpc,127.0.0.1:1337,getMetaData,["latest"])
# e.g.: $(call cita_rpc,127.0.0.1:1337,blockNumber,[])
define cita_rpc
 	@# inc counter
	$(eval RPC_CALL_COUNT=$(shell echo $$(($(RPC_CALL_COUNT)+1))))
	@#echo "RPC_CALL_COUNT: $(RPC_CALL_COUNT)"
	curl -sS  -X POST --data '{"jsonrpc":"2.0","method":"$(2)","params":$(3),"id":$(RPC_CALL_COUNT)}' $(1) | jq '.'
endef

# DEFINE RECEIPES


##@ Dependencies

deps: ## Download the depenedencies.
	$(info Checking and getting dependencies)
	@jq --version || brew install jq || apt-get install jq || (echo "install jq: https://stedolan.github.io/jq/download/" && exit 1)

##@ Cleanup
clean: ## Clean up.
	$(info Cleaning up things, remove all containers/network:)
	docker-compose down

##@ Building

build: clean deps ## Building the base docker image, e.g.: $ make build CITA_VERSION=0.24.0.
	$(info Building the base docker image)
	docker-compose build --build-arg CITA_VERSION=$${CITA_VERSION:=0.24.0} cita_node
	@echo "Run [make check-cita-bin-version] to check bin version"
	@echo "Or run [make run-cita-node-bash] to login the container"

run-cita-node-bash: ## Login a cita_node container and mount dummy dir to /data, useful for debugging CITA node runtime enviroment.
	docker-compose run --rm -v $${PWD}/dummy:/data/ cita_node bash

check-cita-bin-version: ## Check CITA bin version in the base image.
	docker-compose run --rm cita_node bash -c "bin/cita-jsonrpc --version | head -n2"

check-cita-bin-version-all: ## Check CITA all bin version in the base image.
	@cmd="find bin -name cita-* -exec grep -IL . '{}' \; | xargs -I @ sh -c 'echo @ ; @ --version | head -n2; echo'" ;\
		docker-compose run --rm cita_node bash -c "$${cmd}"

config-node: ## Create 1 node config and save to dummy/test-chain.
	docker-compose run --rm -e NODES_CONFIG=$${NODES_CONFIG:=node0:4000} config
	@echo "node config saved at:"
	@ls -d1 dummy/test-chain
	@echo "1. start: $$ make start-node"
	@echo "2. check metaData: $$ make rpc-get-meta-data"
	@echo "3. check blockNumber: $$ make rpc-block-number or $$ make watch target=rpc-block-number"

config-nodes: ## Create 4 nodes config and save to dummy/test-chain, custom nodes e.g.: $ make config-nodes NODES_CONFIG=node0:4000,node1:4000,node2:4000,node3:4000
	docker-compose run --rm -e NODES_CONFIG=$${NODES_CONFIG:=node0:4000,node1:4000,node2:4000,node3:4000} config

start-node: ## Start node0.
	docker-compose up node0

start-nodes: ## Start nodes, start all by default, to start specified nodes e.g.: $ make start-nodes NODES="node0 node3"
	docker-compose up $${NODES:=node0 node1 node2 node3}

stop-nodes: ## Stop nodes, stop all by default, to stop specified nodes e.g.: $ make start-nodes NODES="node3"
	docker-compose stop $${NODES:=}

rpc-get-meta-data: ## Call CITA RPC method getMetaData, e.g.: $ make rpc-get-meta-data RPC_PORT=1337.
	$(call cita_rpc,127.0.0.1:$${RPC_PORT:=1337},getMetaData,["latest"])

rpc-block-number: ## Call CITA RPC method blockNumber, e.g.: $ make rpc-block-number RPC_PORT=1337.
	$(call cita_rpc,127.0.0.1:$${RPC_PORT:=1337},blockNumber,[])

rpc-block-number-all: ## Call CITA RPC method blockNumber for all nodes.
	@chain_dir=dummy/test-chain ;\
	for node_id in `ls -w $${chain_dir} | grep -v template`; do \
		rpc_port=`awk -F '"' '/listen_port = "(1.*)"/{print $$2}' $${chain_dir}/$${node_id}/jsonrpc.toml` ;\
		echo "node$${node_id}: rpc-block-number via rpc_port:$${rpc_port}" ;\
		make rpc-block-number RPC_PORT=$${rpc_port} ;\
		echo ;\
	done

##@ Testing

test: ## Run the unit and intergration testsuites.
test: test-unit test-intergration

test-unit: ## Run the unit testsuite.
	$(info Run the unit testsuite)

test-intergration: ## Run the intergration testsuite.
	$(info Run the intergration testsuite)


##@ Helpers
# helpers are independent recipes, should be able to used in different projects

watch: ## Watch a target, e.g.: $ make watch TARGET=test-block-number
	@if [ "$${TARGET}" == "" ]; then \
		echo "watch which target? .e.g.: make watch TARGET=test-block-number" ;\
	else \
		watch -n 1 -c "make $${TARGET}" ;\
	fi

help:  ## Display help message.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
