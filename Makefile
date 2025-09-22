# Makefile for Gemini HTTP Server

# Variables
PYTHON := python3
PIP := pip3
TEST_DIR := tests
SRC_DIR := gemini_server
REQ_FILE := requirements.txt

# Help target
.PHONY: help
help:
	@echo "Gemini HTTP Server - Development Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make install     - Install dependencies"
	@echo "  make dev         - Run development server"
	@echo "  make test        - Run tests"
	@echo "  make coverage    - Run tests with coverage"
	@echo "  make lint        - Run code linting"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make build       - Build package"
	@echo "  make docs        - Generate documentation"
	@echo "  make docker      - Build and run with Docker"
	@echo "  make help        - Show this help message"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r $(REQ_FILE)
	$(PIP) install pytest pytest-cov flake8 pylint

# Run development server
.PHONY: dev
dev:
	$(PYTHON) main.py

# Run tests
.PHONY: test
test:
	pytest $(TEST_DIR)/ -v

# Run tests with coverage
.PHONY: coverage
coverage:
	pytest $(TEST_DIR)/ --cov=$(SRC_DIR) --cov-report=html --cov-report=term

# Run code linting
.PHONY: lint
lint:
	flake8 $(SRC_DIR)/ $(TEST_DIR)/
	pylint $(SRC_DIR)/

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Build package
.PHONY: build
build:
	$(PYTHON) setup.py sdist bdist_wheel

# Generate documentation
.PHONY: docs
docs:
	@echo "Documentation is available in the docs/ directory"

# Build and run with Docker
.PHONY: docker
docker:
	docker-compose up --build

# Build and run in detached mode
.PHONY: docker-detached
docker-detached:
	docker-compose up -d --build

# Stop Docker containers
.PHONY: docker-stop
docker-stop:
	docker-compose down

# Run security tests
.PHONY: security-test
security-test:
	$(PYTHON) security_tests.py

# Run all tests including security tests
.PHONY: all-tests
all-tests: test security-test

.DEFAULT_GOAL := help