coverage:  ## Run tests with coverage
  coverage erase
  coverage run --include=dadata/* -m pytest -ra
  coverage report -m

deps:  ## Install dependencies
  pip install black coverage flake8 mypy pylint pytest tox

lint:  ## Lint and static-check
  isort .

push:  ## Push code with tags
  git push && git push --tags

test:  ## Run tests
  pytest -ra

## Backend
run-backend:
  uvicorn app:app --reload

## Frontend
install-frontend:
  cd frontend && npm install

run-frontend:
  cd frontend && npm start

## Full project
run-project: run-backend && install-frontend && run-frontend

.PHONY: run-backend install-frontend run-frontend run-project