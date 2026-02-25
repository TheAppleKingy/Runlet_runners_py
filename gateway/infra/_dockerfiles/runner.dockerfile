ARG IMAGE

FROM ${IMAGE}

RUN adduser -D -u 1001 -h /home/sandbox sandbox

WORKDIR /home/sandbox
COPY --from=runner_shared --chown=1001:1001 /runner /usr/local/bin/runner
ENTRYPOINT ["/usr/local/bin/runner"]
