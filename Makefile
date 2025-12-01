DJANGO_PROJECT_DIR := src/notebook

.PHONY: run
run:
	cd $(DJANGO_PROJECT_DIR) && \
	uv run manage.py runserver

.PHONY: makemigrations
makemigrations:
	cd $(DJANGO_PROJECT_DIR) && \
	uv run manage.py makemigrations

.PHONY: migrate
migrate:
	cd $(DJANGO_PROJECT_DIR) && \
	uv run manage.py migrate

.PHONY: shell
shell:
	cd $(DJANGO_PROJECT_DIR) && \
	uv run manage.py shell_plus

.PHONY: startapp
startapp:
	cd $(DJANGO_PROJECT_DIR) && \
	uv run manage.py startapp $(name)