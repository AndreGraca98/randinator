.SILENT: ;
.IGNORE: clean

setup: setup-pre-commit ## Setup project
	pip install -r requirements.txt

setup-pre-commit: ## Setup pre-commit
	pip install pre-commit -U
	pre-commit install
	pre-commit install --hook-type pre-push

test: ## Run tests
	pytest

lint: ## Run linters
	pre-commit run -a

define clean_pattern
	@echo "Removing $(1)"
	find . -name $(1) -exec rm -rf {} +
endef
clean: ## Clean project
	@$(call clean_pattern, '__pycache__')
	@$(call clean_pattern, '.pytest_cache')
	@$(call clean_pattern, '.coverage')
	@$(call clean_pattern, '.ipynb_checkpoints')
	@$(call clean_pattern, 'build')
	@$(call clean_pattern, 'dist')
	@$(call clean_pattern, '*.egg-info')

help: ## Show this help
	@echo "Available commands:"
	awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-30s %s\n", $$1, $$2; }' $(MAKEFILE_LIST)
