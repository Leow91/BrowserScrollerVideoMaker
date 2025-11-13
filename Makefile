.PHONY: help install install-dev setup run gui docker-build docker-run docker-stop clean test lint format

# Default target
help:
	@echo "Scroll Video Generator - Makefile Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install dev dependencies"
	@echo "  make setup         - Complete setup (install + browsers + config)"
	@echo ""
	@echo "Running:"
	@echo "  make run           - Run CLI workflow builder"
	@echo "  make gui           - Start web GUI"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run with Docker Compose"
	@echo "  make docker-stop   - Stop Docker containers"
	@echo "  make docker-logs   - View Docker logs"
	@echo ""
	@echo "Development:"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean temporary files"
	@echo ""
	@echo "Utilities:"
	@echo "  make backup        - Backup workflows and output"
	@echo "  make env           - Generate example .env file"

# Installation
install:
	pip install -r requirements.txt
	playwright install chromium

install-dev:
	pip install -r requirements.txt
	pip install pytest black flake8 isort mypy
	playwright install chromium

# Setup
setup: install
	@echo "Generating example .env file..."
	python config.py
	@echo ""
	@echo "Setup complete! Edit .env file with your settings."
	@echo "Then run 'make gui' to start the web interface."

# Running
run:
	python workflow_builder.py

gui:
	python web_gui.py

# Docker
docker-build:
	docker build -t scroll-video-gen:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

# Development
test:
	@echo "Running tests..."
	pytest -v

lint:
	@echo "Running linters..."
	flake8 *.py --max-line-length=120
	pylint *.py --max-line-length=120 || true

format:
	@echo "Formatting code..."
	black *.py
	isort *.py

# Cleanup
clean:
	@echo "Cleaning temporary files..."
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -f *.pyc
	rm -f temp/*.webm
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"

clean-all: clean
	@echo "Removing output and workflows..."
	rm -rf output/*.mp4
	rm -rf workflows/*.json
	rm -rf logs/*.log

# Utilities
backup:
	@mkdir -p backups/$$(date +%Y%m%d)
	@echo "Creating backup..."
	@cp -r workflows backups/$$(date +%Y%m%d)/ 2>/dev/null || true
	@cp -r output backups/$$(date +%Y%m%d)/ 2>/dev/null || true
	@cp .env backups/$$(date +%Y%m%d)/ 2>/dev/null || true
	@tar -czf backup-$$(date +%Y%m%d).tar.gz backups/$$(date +%Y%m%d)/
	@echo "Backup created: backup-$$(date +%Y%m%d).tar.gz"

env:
	python config.py

# Production
prod-install:
	pip install --no-cache-dir -r requirements.txt
	playwright install chromium
	playwright install-deps chromium

prod-run:
	@echo "Starting production server..."
	python web_gui.py

# Check dependencies
check:
	@echo "Checking FFmpeg..."
	@ffmpeg -version > /dev/null 2>&1 && echo "✓ FFmpeg installed" || echo "✗ FFmpeg not found"
	@echo "Checking Python..."
	@python --version
	@echo "Checking Playwright..."
	@playwright --version 2>/dev/null || echo "✗ Playwright not installed"

# Show stats
stats:
	@echo "=== Project Statistics ==="
	@echo "Workflows: $$(ls -1 workflows/*.json 2>/dev/null | wc -l)"
	@echo "Output videos: $$(ls -1 output/*.mp4 2>/dev/null | wc -l)"
	@echo "Output size: $$(du -sh output 2>/dev/null | cut -f1)"
	@echo "Lines of code: $$(find . -name '*.py' -not -path './venv/*' -exec wc -l {} + | tail -1 | awk '{print $$1}')"
