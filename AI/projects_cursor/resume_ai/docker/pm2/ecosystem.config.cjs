/**
 * PM2: backend (8000) + frontend preview (5173) + AI worker (8765).
 * Host Nginx: use docker/nginx/host.conf → proxies /api, /, /ai
 *
 * From repo root:
 *   chmod +x docker/pm2/*.sh
 *   make pm2-start
 */
const path = require("path");

const repoRoot = path.resolve(__dirname, "../..");
const pm2Dir = __dirname;

module.exports = {
  apps: [
    {
      name: "resume-ai-backend",
      script: path.join(pm2Dir, "run-backend.sh"),
      interpreter: "bash",
      cwd: repoRoot,
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      merge_logs: true,
      error_file: path.join(repoRoot, "logs", "pm2-backend-error.log"),
      out_file: path.join(repoRoot, "logs", "pm2-backend-out.log"),
      time: true,
    },
    {
      name: "resume-ai-frontend",
      script: path.join(pm2Dir, "run-frontend.sh"),
      interpreter: "bash",
      cwd: repoRoot,
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      merge_logs: true,
      error_file: path.join(repoRoot, "logs", "pm2-frontend-error.log"),
      out_file: path.join(repoRoot, "logs", "pm2-frontend-out.log"),
      time: true,
    },
    {
      name: "resume-ai-aiworker",
      script: path.join(pm2Dir, "run-ai.sh"),
      interpreter: "bash",
      cwd: repoRoot,
      instances: 1,
      exec_mode: "fork",
      autorestart: true,
      merge_logs: true,
      error_file: path.join(repoRoot, "logs", "pm2-ai-error.log"),
      out_file: path.join(repoRoot, "logs", "pm2-ai-out.log"),
      time: true,
    },
  ],
};
