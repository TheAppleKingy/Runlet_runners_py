DOCKERFILES_PATH=gateway/infra/_dockerfiles
COMPOSE_DEV=build/dev/compose.yaml
COMPOSE_PROD=build/prod/compose.yaml


runlet.runners.dev.build:
	@docker compose -f ${COMPOSE_DEV} build

runlet.runners.dev.start:
	@docker compose -f ${COMPOSE_DEV} up

runlet.runners.dev.build.start: runlet.runners.dev.build
	@docker compose -f ${COMPOSE_DEV} up

runlet.runners.dev.down:
	@docker compose -f ${COMPOSE_DEV} down

#-------------------------------------------------------------

runlet.runners.prod.build:
	@docker compose -f ${COMPOSE_PROD} build

runlet.runners.prod.start:
	@docker compose -f ${COMPOSE_PROD} up

runlet.runners.prod.build.start: runlet.runners.prod.build
	@docker compose -f ${COMPOSE_PROD} up

runlet.runners.prod.down:
	@docker compose -f ${COMPOSE_PROD} down