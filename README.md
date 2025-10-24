# 🚀 DevOps Microservices CI/CD Project

[![CI/CD Pipeline](https://github.com/Adarsh1337/devops-microservices-cicd/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Adarsh1337/devops-microservices-cicd/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Production-ready DevOps project showcasing Flask API, Docker, Kubernetes, CI/CD with GitHub Actions, Terraform IaC, and comprehensive monitoring. Perfect portfolio for entry-level DevOps positions.**

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Monitoring](#monitoring)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)

## 🎯 Overview

This project demonstrates a complete DevOps workflow for a microservices-based task management application. It includes:

- **Backend API**: Flask-based REST API with PostgreSQL
- **Containerization**: Docker multi-stage builds
- **Orchestration**: Kubernetes manifests with HPA
- **CI/CD**: Automated GitHub Actions pipeline
- **Infrastructure as Code**: Terraform configurations
- **Monitoring**: Prometheus & Grafana integration
- **Best Practices**: Security scanning, testing, logging

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     GitHub Actions CI/CD                      │
│  (Build → Test → Security Scan → Push → Deploy)             │
└─────────────────────┬────────────────────────────────────────┘
                      │
        ┌─────────────▼──────────────┐
        │   Kubernetes Cluster       │
        │  ┌──────────────────────┐  │
        │  │   Ingress Controller │  │
        │  └──────────┬───────────┘  │
        │             │              │
        │  ┌──────────▼───────────┐  │
        │  │   Flask API Pods     │  │
        │  │   (HPA Enabled)      │  │
        │  └──────────┬───────────┘  │
        │             │              │
        │  ┌──────────▼───────────┐  │
        │  │   PostgreSQL         │  │
        │  └──────────────────────┘  │
        │                            │
        │  ┌──────────────────────┐  │
        │  │   Prometheus         │  │
        │  └──────────────────────┘  │
        └────────────────────────────┘
```

## 💻 Technologies

### Backend
- **Flask 2.3.3** - Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **Gunicorn** - WSGI server

### DevOps Tools
- **Docker** - Containerization
- **Kubernetes** - Container orchestration
- **GitHub Actions** - CI/CD pipeline
- **Terraform** - Infrastructure as Code
- **Prometheus** - Metrics collection
- **Grafana** - Visualization

## 📁 Project Structure

```
devops-microservices-cicd/
├── backend/                    # Flask API application
│   ├── app.py                 # Main application file ✅
│   ├── requirements.txt       # Python dependencies ✅
│   ├── Dockerfile             # Multi-stage Docker build
│   ├── .dockerignore          # Docker ignore file
│   └── tests/                 # Unit and integration tests
├── kubernetes/                # K8s manifests
│   ├── deployment.yml         # API deployment
│   ├── service.yml            # Service definition
│   ├── ingress.yml            # Ingress rules
│   ├── configmap.yml          # Configuration
│   ├── secrets.yml            # Secrets (encrypted)
│   ├── hpa.yml                # Horizontal Pod Autoscaler
│   └── postgres/              # PostgreSQL manifests
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions pipeline
├── terraform/                 # Infrastructure as Code
│   ├── main.tf               # Main configuration
│   ├── variables.tf          # Variable definitions
│   ├── outputs.tf            # Output values
│   └── providers.tf          # Provider configuration
├── monitoring/               # Monitoring configuration
│   ├── prometheus.yml        # Prometheus config
│   └── grafana-dashboard.json # Grafana dashboard
├── docker-compose.yml        # Local development setup
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Kubernetes cluster (minikube/kind for local)
- kubectl CLI
- Python 3.9+
- Terraform (optional)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Adarsh1337/devops-microservices-cicd.git
cd devops-microservices-cicd
```

2. **Run with Docker Compose**
```bash
docker-compose up -d
```

3. **Access the API**
```bash
curl http://localhost:5000/health
```

### Manual Setup (Development)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://user:password@localhost:5432/taskdb"
python app.py
```

## 🐳 Docker Deployment

### Build Backend Image
```bash
cd backend
docker build -t devops-task-api:latest .
```

### Run Containers
```bash
docker-compose up -d
```

## ☸️ Kubernetes Deployment

### Deploy to Cluster
```bash
# Apply configurations
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/task-api
```

### Access Application
```bash
# Port forward for local access
kubectl port-forward service/task-api 5000:5000

# Or use Ingress (if configured)
curl http://your-domain.com/api/tasks
```

## 📊 Monitoring

### Prometheus Metrics
The Flask application exposes Prometheus metrics at `/metrics`:
- Request count
- Request duration
- Error rates
- Custom business metrics

### Grafana Dashboards
Import the dashboard from `monitoring/grafana-dashboard.json`

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The pipeline automatically:
1. **Lints** code on every push
2. **Runs tests** with pytest
3. **Security scans** with Trivy
4. **Builds** Docker images
5. **Pushes** to registry
6. **Deploys** to Kubernetes

### Trigger Deployment
```bash
git add .
git commit -m "feat: add new feature"
git push origin main
```

## 🔐 Security Features

- Secret management with Kubernetes Secrets
- Image vulnerability scanning
- Non-root container users
- Resource limits and quotas
- Network policies
- HTTPS/TLS encryption

## 🧪 Testing

```bash
cd backend
pytest tests/ -v --cov=app
```

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/ready` | Readiness probe |
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/:id` | Get specific task |
| PUT | `/api/tasks/:id` | Update task |
| DELETE | `/api/tasks/:id` | Delete task |
| GET | `/metrics` | Prometheus metrics |

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

✅ **Application Development**: REST API design, database integration  
✅ **Containerization**: Docker multi-stage builds, optimization  
✅ **Orchestration**: Kubernetes deployments, services, scaling  
✅ **CI/CD**: Automated pipelines, testing, deployment  
✅ **Infrastructure as Code**: Terraform for cloud resources  
✅ **Monitoring**: Metrics collection, visualization  
✅ **Best Practices**: Security, logging, documentation  

## 🛠️ Next Steps to Complete the Project

To make this project fully functional, create the following files:

### 1. Backend Dockerfile (`backend/Dockerfile`)
```dockerfile
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

### 2. Docker Compose (`docker-compose.yml`)
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: taskdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/taskdb
    depends_on:
      - postgres

volumes:
  postgres_data:
```

### 3. GitHub Actions (`.
