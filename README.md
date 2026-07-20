# 🚛 CDX FreightIQ

**CDX FreightIQ** is an AI-powered logistics planning and recommendation platform developed for the **Central Despatch Division (CDX), Bharat Heavy Electricals Limited (BHEL), Heavy Electrical Equipment Plant (HEEP), Haridwar**. The platform assists logistics planners in selecting suitable transportation solutions, validating Over Dimensional Cargo (ODC), planning industrial packaging, analyzing transportation routes, and querying logistics data through natural language.

The system combines rule-based logistics intelligence with AI-generated explanations to support faster, more consistent, and data-driven shipment planning.

---

# 📌 Problem Statement

Logistics planning requires evaluating multiple factors before selecting an appropriate transportation solution, including:

- Vehicle specifications
- Shipment weight and dimensions
- Route availability
- Transporter information
- Packaging requirements
- ODC compliance

Performing these evaluations manually is time-consuming, repetitive, and susceptible to inconsistencies.

**CDX FreightIQ** addresses this challenge by integrating logistics databases, recommendation engines, and AI-powered assistance into a single decision-support platform capable of producing reliable logistics recommendations within seconds.

---

# ✨ Features

## 🧭 Logistics Dashboard

Provides a real-time overview of logistics operations through interactive analytics.

Features include:

- Total Vehicles
- Available Routes
- Registered Transporters
- ODC vs Non-ODC Vehicle Distribution
- Vehicle Capacity Statistics
- Route Coverage Analysis
- Origin & Destination Analytics
- Interactive Charts and KPIs

---

## 🚚 Vehicle Allocator (Multi-Shipment Optimizer)

Recommends the most suitable trailer based on shipment characteristics.

Capabilities:

- Vehicle recommendation using weight and dimensions
- Mechanical & Hydraulic trailer selection
- Multi-shipment consolidation
- Combined load optimization
- AI-assisted load planning
- Load profile generation
- Axle configuration recommendations
- Vehicle utilization analysis

---

## 📦 AI Packaging Guide

Generates intelligent packaging recommendations based on engineering constraints.

Supports:

- Packaging method recommendation
- Base support recommendation
- Lifting method selection
- Engineering drawing requirements
- Material planning guidance
- ODC detection
- Volume calculation
- Surface area calculation
- Historical packaging lookup
- Special handling recommendations

Considers factors such as:

- Product dimensions
- Weight
- Export shipment
- High-value cargo
- Uneven center of gravity
- Precision surfaces
- Projecting components

---

## 🛣️ Route Intelligence

Provides intelligent route lookup capabilities.

Features:

- Origin to destination distance lookup
- Reverse-route matching
- Distance validation
- Route availability checking

---

## ⚖️ ODC (Over Dimensional Cargo) Checker

Automatically validates whether a shipment exceeds standard vehicle dimensions.

Capabilities:

- ODC detection
- Vehicle suitability verification
- Dimensional validation
- Legal movement assessment

---

## 🤖 Logistics AI Assistant

An AI-powered assistant capable of understanding natural language logistics queries.

Example queries:

- "Recommend a vehicle for 25 MT equipment"
- "Find distance from Agra to Aligarh"
- "Suggest packaging for a transformer"
- "Is this shipment ODC?"

The assistant:

- Extracts shipment parameters
- Detects user intent
- Routes requests to the appropriate logistics engine
- Uses AI to generate professional explanations
- Never fabricates logistics information—responses are based strictly on database and engine outputs

---

## 🗃️ Database Lookup Center

Provides a manual interface for querying logistics master data.

Supports CRUD operations for:

- Vehicles
- Routes
- Transporters

---

# 🏗️ System Architecture

```text
                    Streamlit User Interface
                              │
                              ▼
                    AI Query Orchestrator
                              │
        ┌───────────────┬───────────────┬───────────────┐
        ▼               ▼               ▼               ▼
 Vehicle Engine    Packaging Engine   Route Engine   ODC Engine
        │               │               │               │
        └───────────────┴───────────────┴───────────────┘
                              │
                              ▼
                      SQLite Logistics Database
        ├── Vehicles
        ├── Routes
        ├── Transporters
        ├── Packaging Records
        └── Shipment Data
                              │
                              ▼
                     Groq LLM (Llama 3.3 70B)
                              │
                              ▼
          Professional AI Explanations & Recommendations
```

---

# 🧠 How It Works

### 1. Data Layer

Master logistics datasets (vehicles, routes, transporters, packaging history) are imported into a local SQLite database.

---

### 2. Business Logic Layer

Dedicated recommendation engines process logistics information.

Modules include:

- Vehicle Recommendation Engine
- Packaging Recommendation Engine
- Route Intelligence Engine
- ODC Assessment Engine
- Dashboard Analytics

---

### 3. AI Orchestration Layer

For natural language requests, the orchestrator:

- Extracts shipment details
- Identifies user intent
- Routes requests to the correct engine
- Combines structured outputs

---

### 4. AI Explanation Layer

Structured logistics results are sent to the Groq LLM (`llama-3.3-70b-versatile`) to generate professional explanations while ensuring no unsupported information is introduced.

---

### 5. Presentation Layer

Streamlit provides:

- Interactive dashboards
- Vehicle planning interface
- Packaging planner
- AI chat assistant
- Database lookup tools

---

# ❓ Why RAG Was Not Used

Retrieval-Augmented Generation (RAG) is most effective when information is stored in large collections of unstructured documents such as:

- PDFs
- Manuals
- Reports
- Knowledge bases

CDX FreightIQ primarily relies on **structured relational logistics data**, including:

- Vehicle specifications
- Route distances
- Transporter details
- Packaging history
- Shipment records

Since this information is already available in SQLite tables, using a vector database and document retrieval pipeline would introduce unnecessary complexity.

Instead, the platform directly queries structured data and uses an LLM solely for formatting explanations.

### Benefits

- Faster query execution
- Lower infrastructure complexity
- Accurate structured retrieval
- Deterministic rule-based recommendations
- Reduced operational cost
- No vector database required

---

# 💻 Technology Stack

| Layer | Technology |
|--------|------------|
| Programming Language | Python |
| UI Framework | Streamlit |
| Database | SQLite |
| ORM / Database Toolkit | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| AI Model | Groq (`llama-3.3-70b-versatile`) |
| Configuration | python-dotenv |

---

# 📁 Project Structure

```text
FreightIQ/
├── Home.py
├── pages/
│   ├── 1_Logistics Dashboard.py
│   ├── 2_Logistics AI.py
│   ├── 3_Vehicle Allocator.py
│   ├── 4_Packaging Guide.py
│   └── 5_Database Lookup.py
│
├── ai/
│   ├── orchestrator.py
│   ├── vehicle_engine.py
│   ├── route_optimizer.py
│   ├── odc_checker.py
│   ├── packaging_engine.py
│   ├── data_lookup_engine.py
│   ├── analytics.py
│   ├── axle_calculator.py
│   ├── formatter.py
│   └── gemini_service.py
│
├── database/
│   ├── db.py
│   ├── init_db.py
│   ├── data_lookup_db.py
│   ├── packaging_db.py
│   ├── shipment_service.py
│   └── logistics.db
│
├── vehicle_master.csv
├── distance_data.csv
├── Transporter_updated_details.csv
├── requirements.txt
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

- Python 3.10+
- Groq API Key

---

## Installation

```bash
git clone https://github.com/shruti08-31/FreightIQ.git

cd FreightIQ

pip install -r requirements.txt

pip install groq
```

---

## Environment Configuration

Create a `.env` file:

```text
GROQ_API_KEY=your_api_key_here
```

---

## Initialize Database

```bash
python -m database.init_db
```

The script imports logistics master data into SQLite.

---

## Run the Application

```bash
streamlit run Home.py
```

---

# 🔮 Future Enhancements

- PostgreSQL / MySQL Support
- Real-Time Shipment Tracking
- GIS-Based Route Optimization
- Predictive Logistics Analytics
- Transporter Recommendation Engine
- Automated Logistics Report Generation
- Role-Based Access Control (RBAC)
- Machine Learning-Based Vehicle Recommendation
- Cost Optimization Module

---

# 🎓 Academic Context

This project was developed during a **Summer Internship** at:

**Bharat Heavy Electricals Limited (BHEL)**  
Heavy Electrical Equipment Plant (HEEP)  
Central Despatch Division (CDX)  
Haridwar, Uttarakhand

**Program:**  
B.Tech in Artificial Intelligence and Data Science Engineering

**Specialization:**  
Transportation and Logistics

**Institution:**  
Gati Shakti Vishwavidyalaya

---

# 👩‍💻 Author

**Shruti Prasad**

---

# ⚠️ Disclaimer

This repository contains a demonstration version of the project.

The original application was developed for internal logistics planning within **BHEL's Central Despatch Division (CDX)**. Company-specific operational datasets, proprietary business rules, and confidential logistics information have been removed from this public release.

To adapt the project for another organization, replace the logistics master data files with organization-specific datasets and rebuild the SQLite database using the initialization script.
