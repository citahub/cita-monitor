.DEFAULT_GOAL:=help
SHELL = /bin/sh

# main receipts
.PHONY: deps build clean help
# receipts for Code Quality
.PHONY: code-quality lint-python-code format-python-code lint-shell-code format-shell-code
# receipts for Testing
.PHONY: test test-unit test-intergration

.SILENT: help

##@ Dependencies

deps: ## Download the depenedencies.
	$(info Checking and getting dependencies)
	# install pylint
	@pylint --version || pip install pylint

	# intall yapf
	@yapf --version || pip install yapf

	# intall shfmt
	@(printf "shfmt " && shfmt --version) || brew install shfmt || (echo "Install shfmt: https://github.com/mvdan/sh" && exit 1)

	# intall shellcheck
	@shellcheck --version || brew install shellcheck || apt-get install shellcheck || (echo "install shellcheck: https://github.com/koalaman/shellcheck" && exit 1)

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
	@$(MAKE) lint-python-code
	@$(MAKE) format-python-code

	@$(MAKE) lint-shell-code
	@$(MAKE) format-shell-code

lint-python-code: ## Run linter for python codes
	$(info Run linter for python codes)
	pylint **/*.py

format-python-code: ## Run formatter for python codes.
	$(info Run formatter for python codes)
	cat .style.yapf
	yapf --diff --recursive **/*.py

lint-shell-code: ## Run linter for shell codes.
	$(info Run linter for shell codes)
	find . -name "*.sh" | xargs shellcheck

format-shell-code: ## Run formatter for shell codes.
	$(info Run formatter for shell codes)
	shfmt -i 2 -ci -l .

##@ Helpers

help:  ## Display help message.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
