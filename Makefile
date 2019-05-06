.DEFAULT_GOAL:=help
SHELL = /bin/sh

.PHONY: deps build clean code-quality help
.PHONY: test test-unit test-intergration

.SILENT: help

##@ Dependencies

deps: ## Download the depenedencies.
	$(info Checking and getting dependencies)

##@ Cleanup
clean: ## Clean up.
	$(info Cleaning up things)

##@ Building

build: clean deps ## Compile binary targets.
	$(info Building the project)

##@ Testing

test: ## Run the unit and intergration testsuites.
test: test-unit test-intergration

test-unit: ## Run the unit testsuite.
	$(info Run the unit testsuite)

test-intergration: ## Run the intergration testsuite.
	$(info Run the intergration testsuite)

##@ Code Quality
code-quality: ## Run linter & formatter.
	$(info Run linter & formatter)

##@ Helpers

help:  ## Display help message.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
