build:
	cat ../VERSION | xargs -I @ docker build -t citamon/server --build-arg VERSION="@" .

start:
	ln -s /opt/cita-monitor/server/config/prometheus.yml
	docker run --name citamon_server --rm -it -v /var/run/docker.sock:/var/run/docker.sock --env-file .env citamon/server

shell:
	docker run --name citamon_server --rm -it -v /var/run/docker.sock:/var/run/docker.sock --env-file .env citamon/server sh -l

printenv:
	docker run --name citamon_server --rm -it -v /var/run/docker.sock:/var/run/docker.sock --env-file .env citamon/server printenv

debug:
	docker run --name citamon_server --rm -it -v ${PWD}:/opt/cita-monitor/server -v /var/run/docker.sock:/var/run/docker.sock --env-file .env citamon/server sh -l
