# this file is using for releasing Docker Image to Docker Hub
# IMPORTANT: the order of each directive is important, it will effect image cache
# https://github.com/tiangolo/docker-with-compose
# FROM tiangolo/docker-with-compose
# image size: 442MB

# use docker and docker-compose
# refs: https://github.com/docker/compose/issues/3918#issuecomment-408171838

FROM alpine
# 62.6M
COPY --from=library/docker:latest /usr/local/bin/docker /usr/bin/docker
# 16.7 MB
COPY --from=docker/compose:latest /usr/local/bin/docker-compose /usr/bin/docker-compose
# image size: 108MB

# FROM alpine
# COPY --from=library/docker:latest /usr/local/bin/docker /usr/bin/docker
# 1.7K
# RUN wget -O /usr/local/bin/docker-compose https://github.com/docker/compose/releases/download/1.24.0/run.sh
# RUN chmod +x /usr/local/bin/docker-compose
# image size: 90MB

# Build packages are system packages that are only required for installing
# gems, precompiling assets, etc. They are not included in the final Docker
# image.
# ENV BUILD_PACKAGES \
#     # Required for the sqlite3 gem to compile.
#     sqlite-dev

# Runtime packages are system packages that are required for the application
# to run. They are included in the final Docker image.
# ENV RUNTIME_PACKAGES \
#     # Required for the sqlite3 gem.
#     sqlite-libs git

# Put everything in its own directory.
WORKDIR /opt/cita-monitor

# # Build your application.
# RUN \
#     # Upgrade old packages.
#     # apk --update upgrade && \
#     # Ensure we have ca-certs installed.
#     apk add --no-cache ca-certificates && \
#     # Install build packages.
#     apk add --virtual build-packages build-base $BUILD_PACKAGES && \
#     # Install runtime packages.
#     apk add --virtual runtime-packages nodejs tzdata $RUNTIME_PACKAGES


# Pass CITA_MONITOR_VERSION
ARG VERSION=""
ENV VERSION $VERSION
ENV CITA_MONITOR_DOWNLOAD_URL=https://github.com/citahub/cita-monitor/archive/v${VERSION}.tar.gz
# e.g.: https://github.com/citahub/cita-monitor/archive/v0.4.1.tar.gz

RUN echo "Building CITA Monitor server v${VERSION} with ${CITA_MONITOR_DOWNLOAD_URL}"

# FIXME: `ADD` won't use cache in this case
# ADD ${CITA_MONITOR_DOWNLOAD_URL} v${VERSION}.tar.gz

# RUN curl -L -O -# ${CITA_MONITOR_DOWNLOAD_URL}
# RUN wget -nv ${CITA_MONITOR_DOWNLOAD_URL}
# COPY v0.4.1.tar.gz v0.4.1.tar.gz

# RUN tar zxf v${VERSION}.tar.gz && \
#     rm v${VERSION}.tar.gz


# # Clean up build packages.
# RUN \
#     apk del --purge build-packages && \
#     # Delete APK and gem caches.
#     find / -type f -iname \*.apk-new -delete && \
#     rm -rf /var/cache/apk/* && \
#     rm -rf /usr/local/lib/ruby/gems/*/cache/* && \
#     rm -rf ~/.gem


ENV WORKDIR /opt/cita-monitor/server
WORKDIR ${WORKDIR}

COPY . ${WORKDIR}


# helpers for sh shell
RUN echo '\
    alias ll="ls -lah" \
    ' >> /etc/profile.d/alias.sh && \
    # eneable color prompt
    mv /etc/profile.d/color_prompt /etc/profile.d/color_prompt.sh

# enterpoint
CMD docker-compose build && docker-compose up

# Tips:

# build cita-monitor-server Docker Image:
# cat ../VERSION | xargs -I @ docker build -t citamon/server --build-arg VERSION="@" .

# start citamon server:
# 1. setup env config
# cp .env.example .env

# docker run --rm -it --env-file .env citamon/server

# 2. start server with env config file
# docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock --env-file .env citamon/server

# debug: 
# docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock --env-file .env citamon/server sh -l
