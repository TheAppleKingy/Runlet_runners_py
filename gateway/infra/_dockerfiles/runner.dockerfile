ARG IMAGE

FROM ${IMAGE}

RUN adduser -D -u 1000 -h /home/sandbox sandbox

WORKDIR /home/sandbox

COPY --from=runner_shared --chown=sandbox:sandbox /runner /usr/local/bin/runner

ENTRYPOINT ["/usr/local/bin/runner"]
