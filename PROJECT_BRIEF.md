# 🏙️ Autonomous Real Estate Investment Analyzer

## Project Overview

A full-stack AI-powered web application that autonomously evaluates real estate investment opportunities using a multi-agent pipeline. Each agent specializes in a distinct domain and passes enriched data downstream, culminating in a professional investment memo.

---

## 🎯 Core Concept

> **"From address to investment memo in under 60 seconds."**

Users paste a property address or ZIP code. Five AI agents fire in sequence, each pulling live data from external APIs, and the system returns a structured investment report with ROI, cap rate, risk score, zoning notes, and neighborhood trends.

---

## 🤖 Agent Pipeline (CrewAI + Python Backend)

| # | Agent | Role | Data Sources |
|---|-------|------|--------------|
| 1 | **Market Agent** | Compares neighborhood price trends, comps, median $/sqft | Zillow API, Census API |
| 2 | **Financial Agent** | Computes ROI, Cap Rate, Cash-on-Cash return, break-even | Rentcast API, internal formulas |
| 3 | **Zoning Agent** | Checks zoning codes, permit history, development restrictions | Local Gov APIs, Census TIGER |
| 4 | **Risk Agent** | Evaluates macro trends, vacancy rates, crime index, flood risk | Walk Score API, FEMA, Census |
| 5 | **Report Agent** | Synthesizes all outputs → structured investment memo (PDF/JSON) | GPT-4o (synthesis layer) |

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS + shadcn/ui
- **State:** Zustand
- **Charts:** Recharts / Tremor
- **Auth:** Clerk

### Backend
- **Runtime:** Python (FastAPI)
- **AI Orchestration:** CrewAI
- **LLM:** GPT-4o (via OpenAI API)
- **Task Queue:** Celery + Redis
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL

### External APIs
| API | Purpose |
|-----|---------|
| Zillow (Bridgedata) | Property data, comps, Zestimate |
| Rentcast API | Rental estimates, vacancy rates |
| Walk Score API | Walkability, transit, bike score |
| US Census API | Demographics, income, population trends |
| FEMA Flood Map | Flood zone classification |

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Local Dev:** `localhost:3000` (Next.js) + `localhost:8000` (FastAPI)
- **CI/CD:** GitHub Actions
- **Deployment (prod):** Vercel (frontend) + Railway (backend)

---

## 📁 Folder Structure

```
real-estate-analyzer/
├── frontend/                  # Next.js application
│   ├── app/
│   │   ├── page.tsx           # Landing / Search
│   │   ├── dashboard/         # Results dashboard
│   │   ├── report/[id]/       # Individual investment memo
│   │   └── api/               # Next.js API routes (proxy)
│   ├── components/
│   │   ├── AgentPipeline.tsx  # Live agent status tracker
│   │   ├── MetricsCard.tsx    # ROI / Cap Rate cards
│   │   ├── NeighborhoodMap.tsx
│   │   └── ReportExport.tsx
│   └── package.json
│
├── backend/                   # FastAPI + CrewAI
│   ├── agents/
│   │   ├── market_agent.py
│   │   ├── financial_agent.py
│   │   ├── zoning_agent.py
│   │   ├── risk_agent.py
│   │   └── report_agent.py
│   ├── crews/
│   │   └── investment_crew.py  # CrewAI orchestrator
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── db/
│   │   ├── models.py
│   │   └── database.py
│   ├── services/
│   │   ├── zillow_service.py
│   │   ├── rentcast_service.py
│   │   ├── walkscore_service.py
│   │   └── census_service.py
│   ├── main.py
│   └── requirements.txt
│
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🔑 Environment Variables (.env)

```env
# LLM
OPENAI_API_KEY=

# Real Estate APIs
ZILLOW_API_KEY=
RENTCAST_API_KEY=
WALKSCORE_API_KEY=
CENSUS_API_KEY=

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/realestate

# Redis (Celery)
REDIS_URL=redis://localhost:6379

# Auth
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
```

---

## 🚀 Getting Started (Local Dev)

```bash
# 1. Clone and enter project
git clone https://github.com/yourname/real-estate-analyzer
cd real-estate-analyzer

# 2. Start all services
docker-compose up -d

# 3. Install frontend deps
cd frontend && npm install && npm run dev
# → http://localhost:3000

# 4. Install backend deps
cd ../backend && pip install -r requirements.txt
uvicorn main:app --reload
# → http://localhost:8000

# 5. Run DB migrations
alembic upgrade head
```

---

## 📊 Key Metrics Computed

- **Cap Rate** = Net Operating Income / Property Value × 100
- **Cash-on-Cash Return** = Annual Pre-Tax Cash Flow / Total Cash Invested
- **Gross Rent Multiplier** = Property Price / Annual Gross Rents
- **Break-even Occupancy** = Operating Expenses / Gross Potential Income
- **Risk Score** (0–100) = Weighted composite of macro, crime, vacancy, flood risk

---

## 🗺️ Development Roadmap

### Phase 1 — MVP (Weeks 1–3)
- [ ] Project scaffold (Next.js + FastAPI + Docker)
- [ ] Zillow + Rentcast API integrations
- [ ] Market Agent + Financial Agent
- [ ] Basic dashboard UI

### Phase 2 — Full Pipeline (Weeks 4–6)
- [ ] Zoning Agent + Risk Agent
- [ ] Report Agent (GPT-4o synthesis)
- [ ] PDF export of investment memo
- [ ] PostgreSQL persistence

### Phase 3 — Polish (Weeks 7–8)
- [ ] Auth (Clerk)
- [ ] Saved reports history
- [ ] Portfolio comparison view
- [ ] Deploy to Vercel + Railway

---

## 🧠 AI/LLM Usage

CrewAI manages agent coordination. Each agent has:
- A defined **role**, **goal**, and **backstory**
- Access to specific **tools** (API wrappers)
- Output passed as **context** to the next agent

GPT-4o serves as the reasoning engine for the Report Agent, synthesizing structured JSON from upstream agents into natural-language investment analysis.

---

*Built for serious real estate investors who want data-driven decisions, not gut feelings.*
