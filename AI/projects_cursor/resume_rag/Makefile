.PHONY: help sync stop api frontend run worker redis-up redis-down docker-up docker-down clean test-db connections

PROJECT_ROOT  := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
AI_ROOT       := $(abspath $(PROJECT_ROOT)/../..)
API_PORT      := 8000
FRONTEND_PORT := 8501

.DEFAULT_GOAL := help

help: ## Show available commands
	@echo "Usage: make [target]"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

sync: ## Sync dependencies (uv sync in AI/)
	cd $(AI_ROOT) && uv sync

redis-up: ## Start Redis (local brew or Docker)
	@if redis-cli ping >/dev/null 2>&1; then \
		echo "Redis already running on localhost:6379"; \
	elif command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then \
		docker compose -f $(PROJECT_ROOT)/docker-compose.yml up -d redis; \
		echo "Waiting for Redis on localhost:6379..."; \
		for i in 1 2 3 4 5 6 7 8 9 10; do \
			redis-cli ping 2>/dev/null | grep -q PONG && break; \
			sleep 1; \
		done; \
	else \
		if pgrep -x redis-server >/dev/null 2>&1; then \
			echo "Redis server process found"; \
		else \
			echo "Starting local redis-server..."; \
			redis-server --daemonize yes --port 6379; \
			sleep 1; \
		fi; \
	fi
	@redis-cli ping >/dev/null 2>&1 || (echo "Redis failed to start. Run: redis-server --daemonize yes" && exit 1)
	@echo "Redis is ready"

redis-down: ## Stop Redis container
	docker compose -f $(PROJECT_ROOT)/docker-compose.yml stop redis

wait-api: ## Wait until FastAPI responds on port 8000
	@echo "Waiting for API on http://localhost:$(API_PORT)..."
	@for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 20 25 30; do \
		curl -sf "http://localhost:$(API_PORT)/" >/dev/null 2>&1 && break; \
		sleep 1; \
	done
	@curl -sf "http://localhost:$(API_PORT)/" >/dev/null \
		|| (echo "API did not start on port $(API_PORT). Check logs above." && exit 1)
	@echo "API is ready"

stop: ## Free ports 8000 and 8501, stop worker
	@-lsof -ti :$(API_PORT) | xargs kill -9 2>/dev/null || true
	@-lsof -ti :$(FRONTEND_PORT) | xargs kill -9 2>/dev/null || true
	@-pkill -f "python -m app.jobs.worker" 2>/dev/null || true
	@echo "Ports $(API_PORT) and $(FRONTEND_PORT) cleared, worker stopped"

api: stop redis-up ## Start FastAPI backend only (starts Redis)
	@mkdir -p storage/resumes
	@echo "API: http://localhost:$(API_PORT)/docs"
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port $(API_PORT)'

frontend: ## Start Streamlit frontend only
	@echo "Frontend: http://localhost:$(FRONTEND_PORT)"
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)/frontend" && python -m streamlit run app.py --server.port $(FRONTEND_PORT)'

run: stop redis-up ## Start Redis + RQ worker + API + frontend
	@mkdir -p storage/resumes
	@echo "API:      http://localhost:$(API_PORT)/docs"
	@echo "Frontend: http://localhost:$(FRONTEND_PORT)"
	@echo "Worker:   RQ background jobs (Redis queue)"
	@trap 'kill 0' INT TERM; \
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)" && OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python -m app.jobs.worker' & \
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)" && python -m uvicorn app.main:app --host 0.0.0.0 --port $(API_PORT)' & \
	$(MAKE) wait-api; \
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)/frontend" && python -m streamlit run app.py --server.port $(FRONTEND_PORT)'

worker: redis-up ## Start RQ background worker (requires Redis)
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)" && OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES python -m app.jobs.worker'

docker-up: ## Start full stack with Docker Compose
	docker compose -f $(PROJECT_ROOT)/docker-compose.yml up --build

docker-down: ## Stop Docker Compose stack
	docker compose -f $(PROJECT_ROOT)/docker-compose.yml down

clean: ## Remove local storage only
	rm -rf storage

test-db: ## Test database connection (Snowflake/MySQL)
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)" && python -c "from app.core.database import test_connection; from app.core.config import settings; ok, err = test_connection(); print(\"provider:\", settings.DB_PROVIDER.value); print(\"ok:\", ok); print(\"error:\", err)"'

connections: redis-up ## Log all service connection statuses
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)" && python -c "from app.core.logging_config import setup_logging; setup_logging(); from app.core.connections import log_connection_status; log_connection_status()"'

snowflake-diag: ## Show Snowflake tables, row counts, migration safety
	cd $(AI_ROOT) && uv run sh -c 'cd "$(PROJECT_ROOT)" && PYTHONPATH=. python scripts/snowflake_diag.py'
