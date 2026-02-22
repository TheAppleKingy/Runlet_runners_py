DOCKERFILES_PATH=gateway/infra/_dockerfiles
COMPOSE_DEV=build/dev/compose.yaml

runners.rebuild.store:
	@docker build -f ${DOCKERFILES_PATH}/runner.dockerfile -t runner_store .

#--------------------------------------------------------------------------------------

runlet.runners.dev.build:
	@docker compose -f ${COMPOSE_DEV} build

runlet.runners.dev.start:
	@docker compose -f ${COMPOSE_DEV} up

runlet.runners.dev.build.start: runlet.runners.dev.build
	@docker compose -f ${COMPOSE_DEV} up

runlet.runners.dev.down:
	@docker compose -f ${COMPOSE_DEV} down
