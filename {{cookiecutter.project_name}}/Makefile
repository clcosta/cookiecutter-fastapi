PYTHON_PATH = "python.exe"


.PHONY: install
install: ## Install dependencies

	{% if cookiecutter.python == 'python venv' %}
	@printf "Install with python -m pip\n"
	@$(PYTHON_PATH) -m pip install requirements.txt
	{% else %}
	@printf "Install with poetry\n"
	@poetry install
	{% endif %}


.PHONY: run
run: ## Run API

	@$(PYTHON_PATH) app.py

.PHONY: docs
docs: ## Open documentation for this API-Template

	@$(PYTHON_PATH) -m webbrowser "https://github.com/clcosta/cookiecutter-fastapi"

.PHONY: help
help:
	@printf "Comandos do make\n\n"

	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'