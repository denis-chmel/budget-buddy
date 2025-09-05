# Build the application
build:
	docker-compose build

# Start the application
up:
	docker-compose up -d

# Stop the application
down:
	docker-compose down

# View application logs
logs:
	docker-compose logs -f

# Show help
help:
	@echo "Available commands:"
	@echo "  make build    - Build the application"
	@echo "  make up       - Start the application"
	@echo "  make down     - Stop the application"
	@echo "  make logs     - View application logs"
	@echo "  make help     - Show this help message"

# Set default target
.DEFAULT_GOAL := help
