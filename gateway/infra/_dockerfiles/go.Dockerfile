FROM golang:1.25.6-alpine 

ENV GOCACHE=/tmp/.cache
ENV GOTMPDIR=/tmp
ENV LANG=go
ENV LANGS_CONF_PATH=/runner/languages.yaml

WORKDIR /runner
COPY ../../../languages.yaml .

COPY --from=runner_store /runner /usr/local/bin/runner

ENTRYPOINT ["/usr/local/bin/runner"]
