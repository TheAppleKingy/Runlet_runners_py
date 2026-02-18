DOCKERFILES_PATH=gateway/infra/_dockerfiles

runners.rebuild.store:
	@docker build -f ${DOCKERFILES_PATH}/runner.dockerfile -t runner_store .

runners.rebuild.all: runners.rebuild.store
	@for dockerfile in ${DOCKERFILES_PATH}/*.Dockerfile; do \
		if [ "$$dockerfile" != "${DOCKERFILES_PATH}/runner.dockerfile" ]; then \
			lang=$$(basename $$dockerfile .Dockerfile); \
			echo "🔨 Building $$lang runner..."; \
			docker build -f $$dockerfile -t $${lang}_runner .; \
		fi \
	done

runners.rebuild.lang: runners.rebuild.store
	@if [ -z "$(LANG)" ]; then \
		echo "Please specify LANG (e.g., make runners.rebuild.lang LANG=py)"; \
		exit 1; \
	fi
	docker build -f ${DOCKERFILES_PATH}/$(LANG).Dockerfile -t $(LANG)_runner .