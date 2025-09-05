# Get the current Git version
APP_VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo 'unknown')

# Development commands
build:
	docker-compose build --build-arg APP_VERSION=$(APP_VERSION)

build-clean:
	docker-compose build --build-arg APP_VERSION=$(APP_VERSION) --no-cache

up:
	docker-compose up -d

down:
	docker-compose down

monitor:
	docker-compose logs -f

shell:
	docker-compose run --rm app bash

# Production commands
build-prod:
	docker-compose -f docker-compose.prod.yml build --build-arg APP_VERSION=$(APP_VERSION)

run-prod:
	docker-compose -f docker-compose.prod.yml up --build

down-prod:
	docker-compose -f docker-compose.prod.yml down

# Cloud deployment
deploy-gcp:
	@GIT_VERSION=$$(git describe --tags --always --dirty) && \
	echo "Deploying version: $$GIT_VERSION" && \
	gcloud run deploy budget-buddy \
	  --source . \
	  --platform managed \
	  --update-secrets="DATABASE_URL=budget-buddy-db-creds:latest" \
	  --add-cloudsql-instances="sinuous-concept-471202-t7:us-east1:budget-buddy-db" \
	  --region us-east1 \
	  --project sinuous-concept-471202-t7 \
	  --allow-unauthenticated \
	  --set-env-vars="APP_VERSION=$$GIT_VERSION"

# Database utilities
create-default-user:
	docker-compose run --rm -e PYTHONPATH=/app app python scripts/create_default_user.py

db-shell:
	docker-compose exec db psql -U budgetbuddy -d budgetbuddy

# Help
help:
	@echo "Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  make build               - Build development containers"
	@echo "  make build-clean         - Build development containers without cache"
	@echo "  make up                  - Start development environment"
	@echo "  make down                - Stop development environment"
	@echo "  make monitor             - View application logs"
	@echo "  make shell               - Open bash shell in app container"
	@echo ""
	@echo "Production:"
	@echo "  make build-prod          - Build production containers"
	@echo "  make run-prod            - Run production environment"
	@echo "  make down-prod           - Stop production environment"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-gcp          - Deploy to Google Cloud Run"
	@echo ""
	@echo "Database:"
	@echo "  make create-default-user - Create a default user in the database"
	@echo "  make db-shell            - Open PostgreSQL shell for the database"
	@echo ""
	@echo "  make help                - Show this help message"

# Set default target
.DEFAULT_GOAL := help
