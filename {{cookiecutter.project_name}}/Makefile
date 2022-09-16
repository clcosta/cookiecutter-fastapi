PYTHON_PATH = "python.exe"


.PHONY: install
install: ## Install dependencies

	{% if cookiecutter.python == 'python venv' %}
	@printf "\u1b[32mInstall with \033[1mpip\033[0m\033[m\n"
	@$(PYTHON_PATH) -m pip install -r requirements.txt
	{% else %}
	@printf "\u1b[32mInstall with \033[1mpoetry\033[0m\033[m\n"
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
	@printf "\u1b[32mComandos do make\033[m\n"

	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'