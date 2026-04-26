# 🏛️ AI in RCM — E2E POC

## Regulatory Change Management AI Analyst — Proof of Concept

This POC implements the full **AI in RCM** architecture shown in your slides:
- ✅ In-house Regulatory Feed Ingestion
- ✅ Triage & Applicability Review (AI)
- ✅ Impact Assessment & Gap Analysis (AI)
- ✅ Actionable Recommendations
- ✅ Multi-bank, Multi-regulation batch mode
- ✅ Streamlit GUI matching your screenshot

---

## 🏗️ Architecture

```
rcm_poc/
├── data/
│   └── regulations.py        ← Sample regulations (FCA/PRA) + Bank profiles
├── agents/
│   └── rcm_agent.py          ← AI Gap Analyzer Agent (Claude API)
├── ui/
│   └── app.py                ← Streamlit GUI (5-tab interface)
├── requirements.txt
└── README.md
```

The agent pipeline (mirrors Logical View architecture):
```
Reg Feed → [LLM] Regulation Summary
         → [LLM] Applicability Check     (is this bank in scope?)
         → [LLM] Impact Assessment       (which policies & controls are affected?)
         → [LLM] Gap Analysis            (what's the gap?)
         → [LLM] Action Plan             (what to do, by when, who owns it?)
```

---

## ⚡ Quick Start

### Step 1: Prerequisites
```bash
python --version    # Must be Python 3.10+
pip --version       # pip 23+
```

### Step 2: Clone / set up the project
```bash
# If you downloaded as a folder:
cd rcm_poc

# OR create fresh:
mkdir rcm_poc && cd rcm_poc
# (place all files as per structure above)
```

### Step 3: Create virtual environment
```bash
# Create venv
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 4: Install dependencies
```bash
pip install streamlit anthropic requests pandas plotly
```
> Minimal install — only what's needed to run. Full install: `pip install -r requirements.txt`

### Step 5: Set your Anthropic API key (optional — can also enter in GUI)
```bash
# Mac/Linux
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Windows
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```
> Get your key at: https://console.anthropic.com

### Step 6: Launch the GUI
```bash
streamlit run ui/app.py
```

The app opens automatically at: **http://localhost:8501**

---

## 🖥️ Using the GUI

### Interface Overview (matches your screenshot)

**Left Sidebar:**
- Select Bank (HSBC / Barclays / Lloyds)
- Enter Anthropic API Key
- Regulatory Feed panel — click any regulation to select it

**5 Main Tabs:**
1. **🏦 Bank Profile** — Products, policies, internal controls
2. **📋 Regulation Summary** — Plain English mandate decomposition
3. **✅ Applicability Assessment** — Is this regulation applicable? Score + rationale
4. **📊 Compliance Assessment** — Policy gaps, control gaps, new controls required
5. **🎯 Action Plan** — Prioritised remediation roadmap

**Bottom Bar:**
- `🚀 Run AI Analysis` — Single bank × single regulation
- `🔄 Run All Banks × All Regulations` — Full batch mode
- `⬇️ Export Results (JSON)` — Download analysis output

### Workflow
1. Select a **Bank** from the dropdown
2. Click a **Regulation** in the sidebar feed
3. Enter your **API key**
4. Click **🚀 Run AI Analysis**
5. Navigate tabs to explore results

---

## 🔄 Adding New Regulations

Edit `data/regulations.py` and add to `SAMPLE_REGULATIONS`:

```python
{
    "id": "REG-2026-FCA-002",
    "title": "Your Regulation Title",
    "regulator": "FCA",  # or PRA, Basel, etc.
    "date": "01 March 2026",
    "type": "Policy Statement",
    "source_url": "https://...",
    "full_text": """Full regulation text here...""",
    "mandates": [
        "Mandate 1 text",
        "Mandate 2 text"
    ]
}
```

## 🏦 Adding New Banks

Edit `data/regulations.py` and add to `BANK_PROFILES`:

```python
"YourBank": {
    "name": "Your Bank plc",
    "type": "Retail Bank",
    "jurisdiction": "UK",
    "total_assets": "£500 billion",
    "retail_deposits": "£200 billion",
    "products_services": {
        "Personal Banking": ["Current Accounts", "Mortgages"]
    },
    "policies": ["Policy 1", "Policy 2"],
    "internal_controls": ["Control 1", "Control 2"],
    "regulators": ["FCA", "PRA"]
}
```

---

## 🌐 Real Regulatory Feed (Production Extension)

To scrape real regulations from regulator websites, replace sample data with:

```python
import requests
from bs4 import BeautifulSoup

def scrape_fca_feed():
    url = "https://www.fca.org.uk/news/search-results?start=0&rows=25&sort=date"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, 'lxml')
    # Parse publications...
    return regulations

def scrape_pra_feed():
    url = "https://www.bankofengland.co.uk/prudential-regulation/publications"
    # Similar scraping logic...
```

---

## 📊 Sample Output (JSON)

```json
{
  "summary": {
    "plain_english_summary": "FCA requires banks to...",
    "key_themes": ["Consumer Protection", "Governance"],
    "mandates": [{"mandate_id": "M-001", "plain_english": "..."}]
  },
  "applicability": {
    "is_applicable": true,
    "applicability_score": 92,
    "regulatory_risk_rating": "High",
    "in_scope_business_units": ["Personal Banking", "Wealth Management"]
  },
  "impact": {
    "overall_impact_level": "High",
    "policy_impacts": [...],
    "control_impacts": [...],
    "new_controls_required": [...]
  },
  "action_plan": {
    "total_actions": 8,
    "critical_actions": [...],
    "estimated_cost_impact": "£500k - £1.5m",
    "implementation_roadmap": {...}
  }
}
```

---

## 🚀 Production Roadmap (from your architecture slides)

| Component | POC (This) | Production |
|---|---|---|
| Regulatory Feed | Sample data in Python | Web scrapers + scheduler (cron/Airflow) |
| Vector DB | In-memory | ChromaDB / Pinecone / Azure AI Search |
| LLM | Claude Sonnet via API | Claude with RAG + embedding retrieval |
| GRC Integration | Export JSON | API integration with ServiceNow GRC / Archer |
| Auth | API key in UI | OAuth2 / SSO |
| Deployment | Local Streamlit | Docker + Kubernetes / Azure App Service |
| Monitoring | None | Grafana dashboards + alerting |

---

## 🛠️ Troubleshooting

**Port already in use:**
```bash
streamlit run ui/app.py --server.port 8502
```

**Import errors:**
```bash
# Make sure you're in the rcm_poc directory
cd rcm_poc
streamlit run ui/app.py
```

**API key error:**
- Check key starts with `sk-ant-`
- Verify at console.anthropic.com
- Check billing/credits

**Slow responses:**
- Claude Sonnet processes ~4 LLM calls per analysis (~30-60 seconds)
- Results are cached in session — won't re-run unless cleared

---

## 📦 Dependencies (Minimal)

```
streamlit>=1.42.0     # GUI framework
anthropic>=0.40.0     # Claude API client
requests>=2.31.0      # HTTP client
pandas>=2.2.0         # Data manipulation
plotly>=5.22.0        # Charts (optional)
```
