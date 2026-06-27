.PHONY: setup lint test coverage architecture security ci verify up build down

setup:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio pytest-cov pytest-archon pytest-benchmark ruff black isort mypy bandit pip-audit

lint:
	black --check src tests
	isort --check-only src tests
	ruff check src tests
	mypy src

test:
	pytest tests/

architecture:
	pytest tests/architecture

coverage:
	@echo "Running Domain Coverage (Target 100%)"
	pytest tests/domain --cov=src/domain --cov-fail-under=100 || echo "Coverage target not met: Domain"
	@echo "Running Processing Coverage (Target 95%)"
	pytest tests/processing --cov=src/processing --cov-fail-under=95 || echo "Coverage target not met: Processing"
	@echo "Running Intelligence Coverage (Target 90%)"
	pytest tests/intelligence --cov=src/intelligence --cov-fail-under=90 || echo "Coverage target not met: Intelligence"
	@echo "Running Application Coverage (Target 90%)"
	pytest tests/application --cov=src/application --cov-fail-under=90 || echo "Coverage target not met: Application"
	@echo "Running API Coverage (Target 90%)"
	pytest tests/api --cov=src/api --cov-fail-under=90 || echo "Coverage target not met: API"

security:
	bandit -r src/ -ll -i
	pip-audit -r requirements.txt

ci: lint architecture test security

verify: ci coverage

up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

build:
	docker compose build

down:
	docker compose down -v
