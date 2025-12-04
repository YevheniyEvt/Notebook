
.PHONY: run
run:
	uv run manage.py runserver

.PHONY: makemigrations
makemigrations:
	uv run manage.py makemigrations

.PHONY: migrate
migrate:
	uv run manage.py migrate

.PHONY: shell
shell:
	uv run manage.py shell_plus

.PHONY: startapp
startapp:
	uv run manage.py startapp $(name)