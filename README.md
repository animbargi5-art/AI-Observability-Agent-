# 🚀 TattvaAI

### AI-Powered Incident Investigation Platform

**Transform hours of manual incident investigation into minutes of intelligent analysis**

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)

---

## 🎯 What is TattvaAI?

TattvaAI automates the tedious process of investigating production incidents. Instead of manually searching through traces, logs, and metrics for hours, specialized AI agents work together to quickly identify root causes and provide actionable solutions.

### The Problem
When your production system fails, engineers typically spend 2-4 hours:
- Searching through distributed traces
- Reading thousands of log entries
- Analyzing metric dashboards  
- Checking service dependencies
- Comparing with past incidents

### Our Solution
TattvaAI's AI agents do all of this automatically in under 30 seconds, providing:
- **Root cause analysis** with confidence scores
- **Evidence-based reasoning** across all telemetry
- **Actionable recommendations** for quick fixes
- **Historical pattern matching** for recurring issues

---

## ✨ Key Features

🤖 **Multi-Agent Investigation** - Specialized AI agents for traces, logs, metrics, dependencies, and alerts  
🧠 **Evidence-Based Reasoning** - Every conclusion backed by real telemetry data  
🎯 **Root Cause Analysis** - Automatically identifies likely causes with confidence scores  
📊 **SigNoz Integration** - Native integration with SigNoz observability platform  
⚡ **Fast Results** - Complete investigations in under 30 seconds  
🔄 **Historical Memory** - Learns from past incidents to improve future investigations  

---

## 🚀 Quick Start

### One-Command Setup
```bash
git clone https://github.com/animbargi5-art/AI-Observability-Agent-.git TattvaAI
cd TattvaAI
docker compose up --build -d
```

### Access Your Dashboard
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Health Check
```bash
curl http://localhost:8000/health
```

---

## 🎭 Live Example

### Scenario: E-commerce Checkout Failure
**Problem**: Customers can't complete purchases

**TattvaAI Investigation**:
1. **Trace Agent** → Finds 4.8s latency (400% increase from normal 120ms)
2. **Logs Agent** → Detects Redis timeout errors (143 occurrences)  
3. **Metrics Agent** → Shows 18% error rate, 98% Redis CPU usage
4. **Dependency Agent** → Maps failure: Gateway → Payment → Redis
5. **Historical Agent** → Matches 94% similarity to previous incident

**Result**: Root cause identified as Redis latency causing payment timeouts  
**Confidence**: 96% | **Time**: 28 seconds

**Recommendations**:
- Immediate: Restart Redis cluster
- Short-term: Increase timeout thresholds
- Long-term: Add circuit breaker pattern

---

## 🏗️ Architecture

### Multi-Agent System
```
Incident Report
       ↓
   AI Coordinator
       ↓
   ┌─────────────────┐
   │  Agent Team     │
   │  • Trace Agent  │
   │  • Logs Agent   │  
   │  • Metrics      │
   │  • Dependencies │
   │  • Alerts       │
   │  • Historical   │
   └─────────────────┘
       ↓
  Evidence Analysis
       ↓
  Root Cause Found
       ↓
  Action Plan Ready
```

### Technology Stack
- **Backend**: Python 3.12, FastAPI, LangGraph
- **Frontend**: React 19, TypeScript, Vite
- **AI/ML**: LangChain, Specialized Investigation Agents
- **Observability**: SigNoz, OpenTelemetry, Model Context Protocol
- **Infrastructure**: Docker, PostgreSQL

---

## 🛠️ Development

### Local Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Local Frontend  
```bash
cd frontend
npm install
npm run dev
```

### Environment Setup
Create `backend/.env`:
```env
APP_NAME=TattvaAI
ENVIRONMENT=development
DEBUG=True
SIGNOZ_URL=http://localhost:3301
DEMO_MODE=True
```

---

## 🔧 API Usage

### Start Investigation
```python
import requests

response = requests.post("http://localhost:8000/investigation/start", 
    json={"service_name": "checkout-service"})

print(response.json())
# {
#   "incident_id": "inv_123",
#   "status": "completed", 
#   "confidence": 96,
#   "root_cause": "Redis latency causing payment timeout"
# }
```

### Get Dashboard Stats
```bash
curl http://localhost:8000/dashboard/statistics
```

---

## 📊 Project Structure

```
TattvaAI/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── agents/       # AI investigation agents
│   │   ├── api/          # REST API endpoints  
│   │   ├── graph/        # LangGraph workflows
│   │   ├── signoz/       # SigNoz integration
│   │   └── models/       # Data models
│   └── requirements.txt
├── frontend/             # React TypeScript frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Application pages
│   │   └── services/     # API services
│   └── package.json
├── services/             # Demo microservices
└── docker-compose.yml    # Container orchestration
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`  
5. Open a Pull Request

---

## 🌟 Why TattvaAI?

**For SRE Teams**:
- Reduce MTTR from hours to minutes
- Consistent investigation methodology
- Knowledge preserved across team changes

**For Engineering Teams**:
- Less time firefighting, more time building
- Faster incident resolution
- Improved system reliability

**For Organizations**:
- Lower operational costs
- Better customer experience
- Data-driven incident response

---

## 📈 What's Next

- 🔄 **Auto-Remediation** - Automatically apply fixes for common issues
- 🔍 **Predictive Analysis** - Detect issues before they become incidents  
- 🌐 **Multi-Platform** - Support for Prometheus, Grafana, Jaeger
- 💬 **Chat Interface** - Natural language incident investigation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with amazing open-source tools:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - JavaScript UI library  
- [LangChain](https://langchain.com/) - AI application framework
- [SigNoz](https://signoz.io/) - Open-source observability platform
- [Docker](https://docker.com/) - Containerization platform

---

**Transform your incident response from reactive to intelligent with TattvaAI.**