.DEFAULT_GOAL:=help
SHELL = /bin/sh

# main receipts
.PHONY: deps build clean help
# receipts for Code Quality
.PHONY: code-quality lint-python-code format-python-code lint-shell-code format-shell-code
# receipts for Testing
.PHONY: test test-unit test-intergration
# receipts for Release
.PHONY: changelog changelog-check generate-build-version show-full-version

.SILENT: help

# DEFINE COLOR VARIABLES

INFO_COLOR  = \033[0;36m # Cyan
OK_COLOR    = \033[0;32m # Green
ERROR_COLOR = \033[0;31m # Red
WARN_COLOR  = \033[0;33m # Yellow
NO_COLOR    = \033[m
# more color at https://en.wikipedia.org/wiki/ANSI_escape_code

# DEFINE FUNCTIONS

# print message with ANSI color
# usage:
#   $(call puts,INFO,"This a INFO")
#   $(call puts,OK,"This a OK")
#   $(call puts,ERROR,"This a ERROR")
#   $(call puts,WARN,"This a WARN")
define puts
	echo "${$(1)_COLOR}[$(1)]$(NO_COLOR)" $(2)
endef

##@ Dependencies

deps: ## Download the depenedencies.
	$(info Checking and getting dependencies)
	# install pylint
	@pylint --version || pip install pylint

	# intall yapf
	@yapf --version || pip install yapf

	# install bandit as security linter 
	@bandit --version || pip install bandit

	# intall shfmt
	@(printf "shfmt " && shfmt --version) || brew install shfmt || (echo "Install shfmt: https://github.com/mvdan/sh" && exit 1)

	# intall shellcheck
	@shellcheck --version || brew install shellcheck || apt-get install shellcheck || (echo "install shellcheck: https://github.com/koalaman/shellcheck" && exit 1)

	# install requirements for agent/cita_exporter
	@cd agent/cita_exporter/ && pip3 install -r requirements.txt

##@ Cleanup
clean: ## Clean up.
	$(info Cleaning up things)

##@ Building

build: clean deps ## Compile binary targets.
	$(info Building the project)
	@echo "[build]build all images"
	@make generate-build-version
	@FULL_VERSION=$(shell make show-full-version) ;\
		cd ./server ;\
		[ ! -f .env ] && cp .env.example .env ;\
		docker-compose build --build-arg VERSION="$${FULL_VERSION}"

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
	make lint-python-code-quality
	make lint-python-code-security

lint-python-code-quality: ## Run linter for python codes quality
	@$(call puts,INFO,"Sniffs code smells in Python code")
	pylint $$(git ls-files '*.py')

lint-python-code-security: ## Run linter for python codes security
	@$(call puts,INFO,"Find common security issues in Python code")
	# B605 is "start_process_with_a_shell",B607 is "start_process_with_partial_path", both of them are the way to execute system command。
	# B104 is "hardcoded_bind_all_interfaces", just like 0.0.0.0
	bandit **/*.py -s B605,B607,B104

format-python-code: ## Run formatter for python codes.
	$(info Run formatter for python codes)
	cat .style.yapf
	yapf --diff --recursive $$(git ls-files '*.py')

lint-shell-code: ## Run linter for shell codes.
	$(info Run linter for shell codes)
	shellcheck $$(git ls-files '*.sh')

format-shell-code: ## Run formatter for shell codes.
	$(info Run formatter for shell codes)
	shfmt -i 2 -ci -l .

##@ Continuous Integration

ci: ## Run recipes for CI.
ci: build test code-quality

##@ Release
changelog-check:
	# check local branch
	@git_tags_count=$(shell git log --oneline --decorate | grep "tag:" | wc -l | bc) ; \
		if [ $${git_tags_count} == 0 ]; then \
			echo "No git tags found on current branch, please follow these steps:" ;\
			echo "1. $$ git checkout master" ;\
			echo "2. $$ git checkout -b update-changelog" ;\
			echo "3. $$ git merge develop --no-edit" ;\
			echo "4. $$ make changelog" ;\
			echo "or just run $$ make changelog-auto" ;\
			exit 1 ;\
		fi

changelog: changelog-check ## Generate CHANGELOG.md from git logs.
	$(info How do I make a good changelog? https://keepachangelog.com)
	# auto install git-changelog
	@git-changelog -v || pip3 install git-changelog
	@OUTPUT=CHANGELOG.md ;\
		git-changelog --style basic --template "path:devtools/release/keepachangelog-template" -o $${OUTPUT} . ;\
		git diff $${OUTPUT} ;\
		open $${OUTPUT} ;\
		echo "Edit $${OUTPUT} to keep notable changes"

changelog-auto: ## Auto generate CHANGELOG.md
	$(info Generate CHANGELOG.md in one step)
	# git checkout master
	# git branch -D update-changelog
	# git checkout -b update-changelog
	# git merge develop --no-edit
	git merge master --no-edit
	@$(MAKE) changelog

commit-release-notes: ## Commit VERSION and CHANGELOG.md
	@current_version=`cat VERSION` ;\
	git add VERSION CHANGELOG.md ;\
	git commit -m "bump version to v$${current_version}" ;\
	git log -n 1

bump-version-file: ## Update version number in VERSION file.
	$(info Update version number in VERSION file)
	@[ -x "$$(command -v bumpversion)" ] || pip3 install bumpversion
	@if [ "$${part}" == "" ]; then \
		echo "usage:$$ make bump-version-file part=[major|minor|patch]" ;\
	else \
		echo "Update part: $${part}" ;\
		current_version=`cat VERSION` ;\
		echo "Current version: $${current_version}" ;\
		bumpversion --current-version $${current_version} --allow-dirty $${part} VERSION ;\
		new_version=`cat VERSION` ;\
		echo "New version: $${new_version}" ;\
	fi

generate-build-version: ## Generate build version using format "yyyymmddHHMMSS.commitshortid", e.g.: "20190606201137.40564fe".
	@# build version are only ASCII alphanumerics and hyphen [0-9A-Za-z-] alllowed
	@commitid=$(shell git rev-parse --short HEAD); \
	builddate=$(shell date +"%Y%m%d%H%M%S");  \
	printf "%s.%s" $$builddate $$commitid > .build-version
	@cat .build-version

show-full-version: ## Show product version and build version, e.g.: "v0.3.0+20190606201137.40564fe".
	@product_version=$(shell cat VERSION); \
	build_version=$(shell cat .build-version);  \
	printf "v%s+%s" $$product_version $$build_version

send-pull-request: ## Send a Pull Request with current git branch
	@repo_url=`git ls-remote --get-url` ;\
		user=`echo $${repo_url}|cut -d : -f 2|cut -d / -f 1` ;\
		repo=`echo $${repo_url}|cut -d : -f 2|cut -d / -f 2|cut -d . -f 1` ;\
		current_branch=`git rev-parse --abbrev-ref HEAD` ;\
		pr_url="https://github.com/$${user}/$${repo}/pull/new/$${current_branch}" ;\
		echo "Create a pull request for '$${current_branch}' on GitHub by visiting" ;\
		echo $${pr_url} ;\
		open $${pr_url}

add-release-tag: ## Add git tag using version number from VERSION file
	$(info Add git tag using version number from VERSION file)
	@current_version=`cat VERSION` ;\
		echo "Current version: $${current_version}" ;\
		git tag -a v$${current_version} -m "Release version v$${current_version}" ;\
		latest_tag_commit_id=`git rev-list --tags --max-count=1` ;\
		echo $${latest_tag_commit_id} | xargs git log --oneline --decorate --no-walk ;\
		git tag -n1 | grep v$${current_version}
	@echo "Remember to push tags: $$ git push origin --tags"

##@ Helpers

help:  ## Display help message.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
