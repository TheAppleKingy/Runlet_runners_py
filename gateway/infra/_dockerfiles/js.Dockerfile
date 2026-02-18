FROM node:20-alpine

ENV NODE_ENV=production
ENV TMPDIR=/tmp
ENV HOME=/home/runner
ENV LANG=js
ENV LANGS_CONF_PATH=/runner/languages.yaml

WORKDIR /runner
COPY ../../../languages.yaml .

COPY --from=runner_store /runner /usr/local/bin/runner

ENTRYPOINT ["/usr/local/bin/runner"]

