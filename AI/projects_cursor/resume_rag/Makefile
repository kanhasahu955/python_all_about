.PHONY: help api frontend run worker docker-up docker-down clean

AI_ROOT       := ../..
VENV          := $(AI_ROOT)/.venv
PYTHON        := $(VENV)/bin/python
UVICORN       := $(VENV)/bin/uvicorn
STREAMLIT     := $(VENV)/bin/streamlit
API_PORT      := 8000
FRONTEND_PORT := 8501

.DEFAULT_GOAL := help

help: ## Show available commands
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

api: ## Start FastAPI backend only
	@mkdir -p storage/resumes
	@echo "API: http://localhost:$(API_PORT)/docs"
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port $(API_PORT)

frontend: ## Start Streamlit frontend only
	@echo "Frontend: http://localhost:$(FRONTEND_PORT)"
	cd frontend && $(STREAMLIT) run app.py --server.port $(FRONTEND_PORT)

run: ## Start API + frontend together
	@mkdir -p storage/resumes
	@echo "API:      http://localhost:$(API_PORT)/docs"
	@echo "Frontend: http://localhost:$(FRONTEND_PORT)"
	@trap 'kill 0' INT TERM; \
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port $(API_PORT) & \
	sleep 2; \
	cd frontend && $(STREAMLIT) run app.py --server.port $(FRONTEND_PORT)

worker: ## Start RQ background worker (requires Redis)
	$(PYTHON) -m app.jobs.worker

docker-up: ## Start full stack with Docker Compose
	docker compose up --build

docker-down: ## Stop Docker Compose stack
	docker compose down

clean: ## Remove local storage only
	rm -rf storage
