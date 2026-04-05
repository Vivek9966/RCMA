# 🏦 Financial Regulatory Compliance Agent

An AI-powered system designed to automate compliance analysis for financial documents containing thousands of transactions. This project reduces manual effort in regulatory checks by combining rule-based validation with LLM-driven reasoning.

---

## 🚀 Overview

Financial institutions process massive volumes of transaction data daily. Ensuring compliance with regulatory frameworks (AML, KYC, FATF) is critical but time-consuming.

This project builds an intelligent **Compliance Agent** that:

- 📄 Ingests financial documents (PDF, CSV, statements)
- 🔍 Extracts and structures transaction data
- ⚖️ Applies compliance rules and regulatory checks
- 🧠 Uses LLMs for contextual reasoning and anomaly detection
- 📊 Generates structured compliance reports with explanations

---

## 🧠 System Architecture
```ultree
Input Documents
↓
Data Ingestion & Parsing
↓
Preprocessing (Transaction Structuring)
↓
Compliance Engine
├── Rule-Based Checks
└── LLM Reasoning
↓
Risk Scoring
↓
Report Generation
```

---

## ⚙️ Key Components

### 1. 📄 Ingestion Layer
- Supports PDF, CSV, and structured financial documents
- Converts raw data into machine-readable format

### 2. 🧱 Preprocessing Layer
- Extracts:
  - Transactions
  - Entities (accounts, names)
  - Amounts, timestamps
- Uses deterministic parsing (not fully LLM-dependent)

### 3. 🧠 Compliance Engine

#### 🔹 Rule-Based System
- AML thresholds
- Transaction limits
- Frequency checks

#### 🔹 LLM-Based Reasoning
- Detects suspicious patterns
- Explains compliance violations
- Context-aware analysis

---

### 4. 🔁 Workflow Orchestration (LangGraph)

Pipeline is structured into nodes:

- `document_classifier`
- `transaction_extractor`
- `compliance_checker`
- `risk_scorer`
- `report_generator`

Supports conditional routing:
- High-risk → deeper analysis
- Low-risk → summary output

---

### 5. 📊 Output Layer

- Structured JSON output (for APIs)
- Human-readable compliance reports
- Explainable results with:
  - Triggered rules
  - Evidence (transactions)
  - Reasoning

---

## 🔍 Features

- ✅ Hybrid AI (Rule-based + LLM)
- ✅ Explainable compliance decisions
- ✅ Scalable for large transaction volumes
- ✅ Modular pipeline using LangGraph
- ✅ Evaluation metrics:
  - Faithfulness
  - Answer Relevancy
  - Context Recall
  - Context Precision

---

## 📈 Risk Scoring

Each transaction or document is assigned a risk score based on:

- Transaction amount
- Frequency
- Geographic indicators
- Behavioral anomalies






---

## 🛠️ Tech Stack

- **Backend:** Python, Django REST Framework (DRF)
- **LLM:** LLaMA (via Ollama)
- **Pipeline:** LangGraph
- **Data Processing:** Pandas, NumPy
- **Parsing:** PyMuPDF / Tabula
- **Queue (optional):** Celery + Redis
- **Frontend (optional):** Streamlit / Dashboard

---

## 📦 Installation

```bash
git clone https://github.com/your-username/compliance-agent.git
cd compliance-agent

pip install -r requirements.txt
