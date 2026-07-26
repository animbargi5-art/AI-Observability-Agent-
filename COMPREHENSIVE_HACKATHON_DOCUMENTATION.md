# 🏆 TattvaAI - SigNoz "Agents of SigNoz" Hackathon Submission

**AI-Powered Autonomous Incident Investigation Platform**

---

## 🎯 Executive Summary

**TattvaAI transforms observability data into actionable intelligence through autonomous AI investigation.**

**Problem Statement**: Engineers spend hours manually investigating incidents - searching traces, reading logs, analyzing metrics, and correlating data across multiple tools. This process is time-consuming, error-prone, and dependent on individual expertise.

**Solution**: TattvaAI uses specialized AI agents to autonomously investigate incidents, correlating evidence across traces, logs, metrics, dependencies, and historical data to provide root cause analysis with confidence scores.

**Hackathon Fit**: Built specifically for SigNoz using Model Context Protocol (MCP), showcasing agent-native observability workflows and SRE copilot capabilities.

---

## 🚀 Quick Demo Start (For Judges)

### Prerequisites
- Docker Desktop installed
- 8GB+ RAM available
- Ports 3001, 8000, 8080 available

### 1-Command Setup
```bash
git clone <repository-url>
cd TattvaAI
docker compose up --build -d
```

### Access Points
- **Frontend Dashboard**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **SigNoz**: http://localhost:8080

### Health Check
```bash
curl http://localhost:8000/health
curl http://localhost:8000/dashboard/statistics
```

---

## 🎭 Live Demo Scenarios

### Scenario 1: E-commerce Checkout Failure ⚡
**Problem**: Customers cannot complete purchases
**Investigation Flow**:
1. Open TattvaAI Dashboard
2. Navigate to Investigation page
3. Start investigation for "checkout-service"
4. Watch AI agents work:
   - **Trace Agent**: Finds 4.8s latency (normal: 120ms)
   - **Logs Agent**: Detects Redis timeout errors
   - **Metrics Agent**: Shows 18% error rate spike
   - **Dependency Agent**: Maps Gateway → Payment → Redis flow
   - **Historical Agent**: Matches 94% similar incident #381
5. **Root Cause**: Redis latency → Payment timeout → Checkout failure
6. **Recommendations**: Restart Redis, increase timeouts, add circuit breaker
7. **Confidence**: 96%

### Scenario 2: Database Connection Pool Exhaustion 📊
**Problem**: API responses timing out
**Investigation Flow**:
- AI discovers connection pool exhausted
- Historical data shows similar pattern
- Recommends connection pool scaling

---

## 🏗️ Architecture Highlights

### Multi-Agent Investigation Engine
```
Incident Report
       ↓
  LangGraph Workflow
       ↓
   ┌─────────────────┐
   │  AI Agent Pool  │
   │                 │
   │ • Trace Agent   │  ← Analyzes distributed traces
   │ • Logs Agent    │  ← Searches error patterns
   │ • Metrics Agent │  ← Monitors performance data
   │ • Dependency    │  ← Maps service relationships
   │ • Alert Agent   │  ← Processes active alerts
   │ • Historical    │  ← Matches past incidents
   └─────────────────┘
       ↓
  Evidence Collection
       ↓
  Correlation Engine
       ↓
  Root Cause Analysis (96% confidence)
       ↓
  Actionable Recommendations
```

### SigNoz Integration via MCP
```
TattvaAI Backend
       ↓
 MCP Gateway
       ↓
Official MCP SDK
       ↓
SigNoz MCP Server
       ↓
   SigNoz APIs
       ↓
Observability Data
```

### Technology Stack
- **Backend**: Python, FastAPI, LangGraph, Pydantic
- **AI Orchestration**: LangGraph state machines
- **SigNoz Integration**: Model Context Protocol (MCP)
- **Frontend**: React 19, TypeScript, Vite
- **Infrastructure**: Docker, OpenTelemetry
- **Observability**: Native SigNoz integration

---

## 🎯 SigNoz Hackathon Alignment

### Agent-Native Observability ✅
- **Specialized AI Agents**: Each agent focuses on specific telemetry (traces, logs, metrics)
- **Autonomous Workflows**: No manual dashboard analysis required
- **Evidence-Driven Reasoning**: Transparent AI decision making

### SRE Copilot Capabilities ✅
- **Incident Investigation Automation**: Replaces manual SRE investigation work
- **Historical Memory**: Learns from past incidents
- **Root Cause Identification**: AI determines probable causes
- **Actionable Recommendations**: Suggests specific remediation steps

### AI/LLM Observability Dashboard ✅
- **Investigation Timeline**: Shows AI agent execution
- **Evidence Visualization**: Displays collected telemetry evidence
- **Confidence Scoring**: Quantifies AI certainty
- **Decision Transparency**: Explainable investigation process

### Native SigNoz Integration ✅
- **MCP Protocol**: Uses official Model Context Protocol
- **Full Telemetry Access**: Traces, logs, metrics, dependencies, alerts
- **SigNoz MCP Server**: Leverages official SigNoz tooling
- **Provider Independence**: Clean abstraction layer

---

## 🔧 Technical Implementation

### Core Components

#### 1. AI Agent Architecture
```python
# Specialized agents for different telemetry
class TraceAgent:
    def investigate(self, state: InvestigationState) -> Evidence:
        traces = self.trace_tool.search_traces(service_name, time_range)
        return self.analyze_latency_patterns(traces)

class LogsAgent:
    def investigate(self, state: InvestigationState) -> Evidence:
        logs = self.logs_tool.search_logs(service_name, error_patterns)
        return self.extract_error_evidence(logs)
```

#### 2. LangGraph Orchestration
```python
workflow = StateGraph(InvestigationState)
workflow.add_node("trace_agent", trace_analysis)
workflow.add_node("logs_agent", log_analysis)
workflow.add_node("correlation", correlate_evidence)
workflow.add_node("root_cause", determine_cause)
workflow.compile()
```

#### 3. MCP Integration
```python
class MCPGateway:
    def execute_tool(self, tool_name: str, params: dict):
        return self.mcp_client.call_tool(tool_name, params)
        
# SigNoz tool execution
traces = mcp_gateway.execute_tool("search_traces", {
    "service_name": "checkout-service",
    "time_range": "1h"
})
```

#### 4. Evidence Collection
```python
@dataclass
class Evidence:
    source: str          # "TraceAgent", "LogsAgent"
    category: str        # "Performance", "Error"
    severity: str        # "HIGH", "MEDIUM", "LOW"
    finding: str         # "Latency increased 400%"
    confidence: float    # 0.95
    data: dict          # Supporting telemetry
    timestamp: datetime
```

---

## 📊 Demo Data & Results

### Investigation Metrics
- **Evidence Pieces Collected**: 14 across all telemetry sources
- **Investigation Time**: <30 seconds end-to-end
- **Root Cause Confidence**: 96%
- **Historical Match Accuracy**: 94% similarity to incident #381
- **Agent Execution**: All 6 agents complete successfully

### Evidence Correlation
```
Trace Evidence:    4.8s latency (400% increase)
Log Evidence:      Redis timeout errors (143 occurrences)
Metric Evidence:   18% error rate, 98% CPU usage
Dependency:        Gateway → Payment → Redis chain
Historical:        94% match to previous Redis incident
Alert Evidence:    Critical database timeout alerts
```

### Generated Recommendations
1. **Immediate**: Restart Redis cluster
2. **Short-term**: Increase connection timeout thresholds
3. **Medium-term**: Implement circuit breaker pattern
4. **Long-term**: Scale Redis with read replicas
5. **Monitoring**: Add Redis latency alerts

---

## 🏅 Innovation Highlights

### 1. Multi-Agent Architecture
- **Novel Approach**: Distributes investigation across specialized agents
- **Modular Design**: Each agent can be developed/tested independently
- **Explainable AI**: Every conclusion backed by evidence

### 2. Evidence-Driven Reasoning
- **Transparent Process**: No black-box AI decisions
- **Confidence Scoring**: Quantified certainty levels
- **Audit Trail**: Complete investigation timeline

### 3. Historical Memory Integration
- **Pattern Recognition**: Learns from past incidents
- **Similarity Matching**: Identifies recurring problems
- **Solution Reuse**: Suggests previously successful fixes

### 4. Native MCP Implementation
- **Standards Compliance**: Uses official Model Context Protocol
- **Future-Proof**: Extensible to other observability providers
- **Tool Abstraction**: Clean separation of concerns

---

## 📈 Impact & Value Proposition

### For SRE Teams
- **Faster MTTR**: Automated investigation reduces resolution time
- **Knowledge Preservation**: Historical incidents become searchable
- **Skill Democratization**: Junior engineers access senior expertise
- **Consistent Process**: Standardized investigation methodology

### For Platform Engineers
- **Operational Efficiency**: Less manual dashboard analysis
- **Proactive Insights**: Historical patterns reveal systemic issues
- **Scalable Operations**: AI handles increasing service complexity
- **Data-Driven Decisions**: Evidence-based recommendations

### For Engineering Organizations
- **Reduced Toil**: Automates repetitive investigation work
- **Improved Reliability**: Faster, more accurate incident response
- **Cost Optimization**: Reduces engineer time spent on manual analysis
- **Learning Organization**: Institutional memory in AI form

---

## 🚀 Production Readiness

### Current Implementation
✅ **Working End-to-End**: Complete investigation pipeline  
✅ **Docker Deployment**: Production-ready containerization  
✅ **SigNoz Integration**: Native MCP connectivity  
✅ **Demo Data**: Realistic investigation scenarios  
✅ **API Documentation**: OpenAPI/Swagger specs  
✅ **Health Monitoring**: System status endpoints  

### Scalability Considerations
- **Stateless Architecture**: Horizontal scaling ready
- **Async Processing**: Non-blocking investigation workflow
- **Caching Layer**: Optimized telemetry retrieval
- **Rate Limiting**: Respects SigNoz API limits

### Security & Reliability
- **Environment Configuration**: Secure secrets management
- **Error Handling**: Graceful degradation
- **Logging & Monitoring**: Observable investigation process
- **Authentication Ready**: RBAC framework prepared

---

## 🎯 Demo Script (10-15 minutes)

### Opening (2 minutes)
"TattvaAI solves a critical problem: engineers spend hours manually investigating production incidents. Instead of searching through traces, logs, and metrics manually, TattvaAI uses AI agents to automatically investigate incidents and provide root cause analysis."

### Architecture Overview (3 minutes)
- Show multi-agent architecture diagram
- Explain SigNoz integration via MCP
- Demonstrate modular, explainable approach

### Live Investigation (5 minutes)
- Open TattvaAI dashboard
- Start checkout-service investigation
- Show agents executing in real-time
- Display evidence collection
- Review root cause determination
- Show confidence scoring

### Technical Deep Dive (3 minutes)
- Backend API responses
- MCP tool execution
- Evidence correlation process
- Historical matching algorithm

### Q&A (2-5 minutes)
- Architecture questions
- Scaling considerations
- SigNoz integration details
- Future roadmap

---

## 🔮 Future Roadmap

### Phase 1 (Current): Foundation ✅
- Multi-agent investigation engine
- SigNoz MCP integration
- Evidence-driven reasoning
- Working demo deployment

### Phase 2: Enhanced Intelligence
- **Advanced ML Models**: Custom incident classification
- **Predictive Analytics**: Proactive failure detection  
- **Auto-Remediation**: Automated fix execution
- **Multi-Provider Support**: Prometheus, Grafana, Jaeger

### Phase 3: Enterprise Features
- **RBAC Integration**: Role-based access control
- **Investigation Workflows**: Custom organization processes
- **Compliance Reporting**: Audit trail exports
- **Team Collaboration**: Shared investigation workspace

### Phase 4: AI Evolution
- **Natural Language Interface**: Chat-based investigation
- **Autonomous Response**: Self-healing systems
- **Cross-System Correlation**: Infrastructure + application
- **Continuous Learning**: Feedback-driven improvement

---

## 📋 Evaluation Criteria Alignment

### Technical Innovation (25%)
✅ **Multi-agent architecture**: Novel approach to investigation  
✅ **MCP integration**: Cutting-edge protocol implementation  
✅ **Evidence-driven AI**: Transparent reasoning process  
✅ **LangGraph orchestration**: Advanced workflow management  

### SigNoz Integration (25%)  
✅ **Native MCP usage**: Proper protocol implementation  
✅ **Full telemetry access**: Traces, logs, metrics, dependencies  
✅ **Real workflows**: Production-ready investigation process  
✅ **Extensible design**: Additional provider support ready  

### Practical Impact (25%)
✅ **SRE productivity**: Automates manual investigation  
✅ **Faster MTTR**: Reduces incident resolution time  
✅ **Knowledge preservation**: Historical incident memory  
✅ **Scalable operations**: Handles complex distributed systems  

### Demo Quality (25%)
✅ **Live functionality**: Working end-to-end system  
✅ **Clear problem statement**: Addresses real pain points  
✅ **Technical depth**: Sophisticated architecture  
✅ **Production readiness**: Docker deployment ready  

---

## 📞 Contact & Repository

### Repository Access
- **GitHub**: [TattvaAI Repository](repository-url)
- **Documentation**: Comprehensive README and architecture docs
- **Demo Scripts**: Ready-to-run Docker Compose setup
- **API Docs**: OpenAPI specifications included

### Technical Contact
- **Architecture Questions**: See detailed documentation
- **SigNoz Integration**: Native MCP implementation
- **Deployment**: Docker Compose ready
- **Extensions**: Modular agent framework

---

## 🏆 Competition Advantages

### Unique Differentiators
1. **Only multi-agent investigation platform** in competition
2. **Native MCP implementation** showcasing protocol correctly
3. **Evidence-driven reasoning** with transparency
4. **Historical memory integration** for learning
5. **Production-ready deployment** with Docker

### Technical Sophistication
- **LangGraph orchestration**: Advanced AI workflow management
- **Modular architecture**: Each component independently testable
- **Clean abstractions**: Provider-independent design
- **Comprehensive observability**: Self-monitoring investigation process

### Practical Value
- **Real SRE problem**: Addresses actual engineering pain
- **Immediate impact**: Reduces investigation time from hours to minutes
- **Scalable solution**: Handles increasing system complexity
- **Knowledge preservation**: Organizational learning in AI form

---

**TattvaAI represents the future of observability: transforming data into understanding through autonomous AI investigation.**

*Built specifically for the SigNoz "Agents of SigNoz" hackathon - showcasing agent-native observability workflows powered by the Model Context Protocol.*