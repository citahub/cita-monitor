# CITA-Monitor

A Prometheus project to monitor running status of [CITA](https://github.com/cryptape/cita).

Metrics are including blockchain data, process status, host info like CPU/memory/disk usage etc.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

* Docker: [install Docker guide](https://docs.docker.com/install/)
* Python: [install Python guide](https://docs.python-guide.org/starting/installation/)

### Installing

PENDING: for installing server, read [server/README.md](server/README.md)

PENDING: screen shots for server

PENDING: for installing agent, read [agent/README.md](agent/README.md)

PENDING: screen shots for agent


## Acknowledgments

* Prometheus: https://prometheus.io/
* Prometheus node-exporter: https://github.com/prometheus/node_exporter
* Prometheus process-exporter: https://github.com/ncabatoff/process-exporter
* Prometheus rabbitmq-exporter: https://github.com/kbudde/rabbitmq_exporter
* CITA: http://docs.citahub.com
* Docker: https://www.docker.com/

## Contributing

### Creating a Bug Report

open a new issue: https://github.com/cryptape/cita-monitor/issues/new 

with your version info

### Get source

```
git clone git@github.com:cryptape/cita-monitor.git
```

### Coding style

#### Coding style for Shell

* coding style guide: [Google Shell Style guide](https://google.github.io/styleguide/shell.xml)
* code formatter: [`shfmt -i 2 -ci`](https://github.com/mvdan/sh#shfmt), vscode extension: shell-format
* linter: [ShellCheck](https://github.com/koalaman/shellcheck), vscode extension: shell-format


#### Coding style for Python

* coding style guide: http://google.github.io/styleguide/pyguide.html
* code formatter: [yapf](https://github.com/google/yapf)
* linter: [pylint](https://www.pylint.org/)

#### Coding style for Docker

* coding style guide: https://github.com/Haufe-Lexware/docker-style-guide
* formatter: https://www.fromlatest.io/
* best-practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/

#### Coding style for Makefile

* coding style guide: https://style-guides.readthedocs.io/en/latest/makefile.html
* tutorial: https://makefiletutorial.com/
* conventions: https://www.gnu.org/prep/standards/html_node/Makefile-Conventions.html
* best-practices: https://suva.sh/posts/well-documented-makefiles/

### Running the tests

PENDING: Explain how to run the automated tests for this system


### Commit your changes

#### Workflow

[GitHub Flow](https://help.github.com/en/articles/github-flow), [Understanding the GitHub flow](https://guides.github.com/introduction/flow/)

#### git style guide

use [git-style-guide](https://github.com/agis/git-style-guide) for Branches, Commits,Messages, Merging


## Versioning

We use [SemVer](http://semver.org/) for versioning.

## License

This project is licensed under the Apache 2.0 License
