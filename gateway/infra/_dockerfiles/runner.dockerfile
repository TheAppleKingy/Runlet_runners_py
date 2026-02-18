FROM golang:1.25.6-alpine AS builder

WORKDIR /runner

COPY ../../../runner/go.mod ../../../runner/go.sum ./
RUN go mod download

COPY ../../../runner .

RUN CGO_ENABLED=0 GOOS=linux go build -o runner ./cmd/runner

FROM scratch AS runner_store
COPY --from=builder /runner/runner /runner
