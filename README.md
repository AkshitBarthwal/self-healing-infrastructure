
# Self-Healing Infrastructure with Docker, Prometheus & Alertmanager

## 📌 Project Overview

This project implements a self-healing infrastructure system that monitors
an NGINX service, detects failures, and triggers automated recovery through
Prometheus, Alertmanager, and a custom Python webhook.

## 🏗️ Architecture

NGINX → Prometheus → Alert Rules → Alertmanager → Webhook Receiver → Docker API → NGINX Restart

### Components

- **NGINX:** Web service being monitored.
- **Prometheus:** Collects metrics and evaluates alert rules.
- **Node Exporter:** Exposes host system metrics.
- **cAdvisor:** Provides container metrics.
- **Blackbox Exporter:** Performs endpoint health checks.
- **Alertmanager:** Groups and routes alerts.
- **Python Webhook:** Authenticates incoming alerts and triggers recovery.
- **Docker:** Runs the services and allows the webhook to restart NGINX.

## 🛠️ Technologies Used

- Docker and Docker Compose
- Prometheus
- Alertmanager
- Python
- NGINX
- Node Exporter
- cAdvisor
- Blackbox Exporter
- Linux and Bash

## ⚙️ Project Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd self-healing-infrastructure
```

### 2. Configure secrets

Create the webhook token using the project's setup instructions.
Do not commit secrets to GitHub.

### 3. Start the infrastructure

```bash
docker compose up -d --build
```

### 4. Verify containers

```bash
docker compose ps
```

### 5. Access monitoring services

- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- NGINX: http://localhost:8081

## 🧪 Testing & Results

| Test | Result |
|---|---|
| Docker services startup | Verified |
| NGINX health check | Healthy |
| Prometheus alert configuration | Configured |
| Webhook authentication | Verified with an earlier test |
| Manual recovery test | Successful |
| NGINX restart after alert | Successful in earlier test |
| Cooldown behavior | Pending verification |
| Latest Alertmanager notification delivery | Pending verification |

## 📸 Screenshots

Screenshots are available in the `screenshots/` directory.

They demonstrate project configuration, monitoring, alert rules,
webhook processing, and recovery tests.

## 🔐 Security

- Webhook authentication uses a bearer token.
- Secrets are stored outside version-controlled source files.
- The webhook uses Docker access to restart the target container.
- Docker socket access carries significant privileges and should be restricted.

## 📚 What I Learned

- Monitoring services using Prometheus.
- Configuring alert rules and Alertmanager.
- Building a Python webhook receiver.
- Automating service recovery with Docker.
- Testing alert-driven recovery workflows.
- Handling authentication and secrets in a containerized environment.

## 👨‍💻 Author

Akshit Barthwal
