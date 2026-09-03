.PHONY: help up down build restart logs migrate seed createsuperuser test test-backend test-frontend clean

help:
	@echo "FavvMenuz Makefile Commands:"
	@echo "  make up              Start all containers in detached mode"
	@echo "  make down            Stop and remove containers"
	@echo "  make build           Rebuild Docker images"
	@echo "  make restart         Restart all services"
	@echo "  make logs            Tail logs from all services"
	@echo "  make migrate         Run Django migrations inside backend container"
	@echo "  make seed            Seed demo restaurant and menu data"
	@echo "  make createsuperuser Create a Django administrative user"
	@echo "  make test            Run all backend and frontend tests"
	@echo "  make test-backend    Run Django backend test suite"
	@echo "  make test-frontend   Run frontend typecheck and linting"
	@echo "  make clean           Remove temporary build artifacts and caches"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

restart:
	docker compose restart

logs:
	docker compose logs -f

migrate:
	docker compose exec backend python manage.py migrate

seed:
	docker compose exec backend python manage.py seed_demo_data

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

test: test-backend test-frontend

test-backend:
	docker compose exec backend python manage.py test

test-frontend:
	cd frontend && npm run build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
