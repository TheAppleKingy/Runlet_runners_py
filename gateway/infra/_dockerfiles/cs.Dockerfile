FROM frolvlad/alpine-mono:latest

ENV LANG=cs
ENV LANGS_CONF_PATH=/runner/languages.yaml

WORKDIR /runner
COPY ../../../languages.yaml .

COPY --from=runner_store /runner /usr/local/bin/runner

ENTRYPOINT ["/usr/local/bin/runner"]
