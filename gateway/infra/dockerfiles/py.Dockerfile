FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=py
ENV LANGS_CONF_PATH=/runner/languages.yaml

WORKDIR /runner
COPY ../../../languages.yaml .

COPY --from=runner_store /runner /usr/local/bin/runner

ENTRYPOINT ["/usr/local/bin/runner"]
