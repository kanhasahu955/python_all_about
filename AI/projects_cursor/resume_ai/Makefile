# Resume AI — local dev, Docker (nginx+fe+be+ai), PM2+Nginx (host)
#
# Variables (override: `make VENV=.venv install`)
PYTHON       ?= python3
VENV         ?= venv
PIP          := $(VENV)/bin/pip
UVICORN      := $(VENV)/bin/uvicorn
BACKEND_DIR  := backend
FRONTEND_DIR := frontend
COMPOSE      ?= docker compose

.PHONY: help install install-fe dev fe-dev docker-build docker-up docker-down docker-logs docker-ps \
	pm2-start pm2-restart pm2-stop pm2-logs nginx-print-host

help:
	@echo "Targets:"
	@echo "  make install          Backend venv + pip install"
	@echo "  make install-fe       Frontend npm install"
	@echo "  make dev              Backend API reload :8000"
	@echo "  make fe-dev           Frontend Vite dev :5173 (proxies /api,/health,/ai)"
	@echo "  make docker-build     Build Compose images (docker/docker-compose.yml)"
	@echo "  make docker-up        Stack: nginx:80 → frontend + backend + ai"
	@echo "  make docker-down      Stop stack"
	@echo "  make docker-logs      Follow logs"
	@echo "  make pm2-start        PM2: backend:8000, frontend:5173, ai:8765"
	@echo "  make pm2-restart      Restart PM2 apps from docker/pm2/ecosystem.config.cjs"
	@echo "  make pm2-stop         Delete those PM2 apps"
	@echo "  make pm2-logs         Tail PM2 logs"
	@echo "  make nginx-print-host Install host Nginx (→ docker/nginx/host.conf)"

$(VENV)/bin/pip:
	$(PYTHON) -m venv $(VENV)

install: $(VENV)/bin/pip
	$(PIP) install --upgrade pip
	$(PIP) install -r $(BACKEND_DIR)/requirements.txt
	@mkdir -p logs

install-fe:
	cd $(FRONTEND_DIR) && npm install

dev: install
	cd $(BACKEND_DIR) && PYTHONPATH=. ../$(UVICORN) main:app --reload --host 0.0.0.0 --port 8000

fe-dev: install-fe
	cd $(FRONTEND_DIR) && npm run dev

docker-build:
	$(COMPOSE) build

docker-up:
	@mkdir -p logs
	$(COMPOSE) up -d

docker-down:
	$(COMPOSE) down

docker-logs:
	$(COMPOSE) logs -f

docker-ps:
	$(COMPOSE) ps

pm2-start: install install-fe
	@mkdir -p logs
	@chmod +x docker/pm2/run-backend.sh docker/pm2/run-frontend.sh docker/pm2/run-ai.sh
	pm2 start docker/pm2/ecosystem.config.cjs

pm2-restart:
	pm2 restart resume-ai-backend resume-ai-frontend resume-ai-aiworker

pm2-stop:
	-pm2 delete resume-ai-backend resume-ai-frontend resume-ai-aiworker

pm2-logs:
	pm2 logs

nginx-print-host:
	@echo "Host Nginx → PM2 (frontend :5173, backend :8000, AI :8765):"
	@echo "  sudo cp docker/nginx/host.conf /etc/nginx/sites-available/resume-ai"
	@echo "  sudo ln -sf /etc/nginx/sites-available/resume-ai /etc/nginx/sites-enabled/"
	@echo "  sudo nginx -t && sudo systemctl reload nginx"
