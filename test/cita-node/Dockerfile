# IMPORTANT: the order of each directive is important, it will effect image cache

FROM cita/cita-run:ubuntu-18.04-20190419

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
WORKDIR /opt/cita-run
ENV APP_HOME /opt/cita-run

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


# Pass CITA_VERSION
ARG CITA_VERSION=""
ENV CITA_VERSION $CITA_VERSION
ENV CITA_DOWNLOAD_URL=https://github.com/cryptape/cita/releases/download/v${CITA_VERSION}/cita_secp256k1_sha3.tar.gz

# ADD ${CITA_DOWNLOAD_URL} cita_secp256k1_sha3.tar.gz
# RUN tar zxf cita_secp256k1_sha3.tar.gz

# FIXME: `ADD` won't use cache in this case
RUN curl -L -O -# ${CITA_DOWNLOAD_URL} && tar zxf cita_secp256k1_sha3.tar.gz
RUN rm cita_secp256k1_sha3.tar.gz

# # Clean up build packages.
# RUN \
#     apk del --purge build-packages && \
#     # Delete APK and gem caches.
#     find / -type f -iname \*.apk-new -delete && \
#     rm -rf /var/cache/apk/* && \
#     rm -rf /usr/local/lib/ruby/gems/*/cache/* && \
#     rm -rf ~/.gem


# Alpine Linux's Ash shell will automatically source the /etc/profile script each time the shell is launched
ENV ENV="/etc/profile"
COPY cita-node/docker-init /usr/sbin/
RUN echo source /usr/sbin/docker-init >> /etc/profile

ARG CITA_NODE_ID=""
ENV CITA_NODE_ID $CITA_NODE_ID

ENV WORKDIR /opt/cita-run/cita_secp256k1_sha3
WORKDIR ${WORKDIR}
ENV PATH "$PATH:$WORKDIR/bin:$WORKDIR/scripts"

# bugfix NODE_PATH in bin/cita script for CITA v0.24.0
# ref: https://github.com/cryptape/cita/issues/626
RUN sed -i 's/NODE_PATH=/NODE_PATH="$(realpath ${NODE_NAME})" # was: /' ${WORKDIR}/bin/cita

# auto setup and start CITA service with config "test-chain/$CITA_NODE_ID"
CMD bash -c 'if [ -d /data/test-chain/$CITA_NODE_ID ]; then cd /data/; cita bebop setup test-chain/$CITA_NODE_ID; cita bebop start test-chain/$CITA_NODE_ID; cita bebop logs test-chain/$CITA_NODE_ID chain; fi;'
