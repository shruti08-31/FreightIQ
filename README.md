# FreightIQ: AI Logistics Planning & Recommendation System

## Overview

FreightIQ is an AI-powered Logistics Planning and Recommendation System developed to assist logistics planners in making informed transportation decisions. The platform combines logistics databases, rule-based recommendation engines, route intelligence, packaging planning, and AI-powered analysis into a single decision-support system.

The application helps users evaluate shipment requirements based on cargo weight, dimensions, route information, transporter availability, and packaging constraints while generating intelligent logistics recommendations.

---

## Key Features

### Logistics Dashboard

* Fleet inventory analytics
* Route database statistics
* Transporter information
* ODC-capable fleet insights
* Logistics network coverage analytics

### Vehicle Recommendation Engine

* Vehicle allocation based on cargo dimensions
* Weight-based vehicle selection
* Capacity validation
* Alternative vehicle recommendations

### ODC Assessment Engine

* Over-Dimensional Cargo (ODC) identification
* Cargo dimension validation
* Vehicle suitability assessment
* Compliance recommendations

### Route Intelligence Engine

* Approved route lookup
* Distance analysis
* Origin and destination validation
* Route availability checks

### Packaging Planning Assistant

* Packaging type recommendation
* Material planning requirements
* Engineering drawing assessment
* Volume and surface area calculations
* Fragility-based packaging suggestions

### AI Logistics Assistant

* Natural language interaction
* Shipment analysis
* Vehicle recommendation explanations
* Route and logistics guidance
* AI-powered recommendation reasoning

### Database Lookup Center

* Route information lookup
* Vehicle database exploration
* Transporter information access
* Logistics data search capabilities

---

## System Architecture

```text
User Interface (Streamlit)
            │
            ▼
Business Logic Layer
├── Vehicle Recommendation Engine
├── ODC Assessment Engine
├── Route Intelligence Engine
├── Packaging Planning Engine
└── Dashboard Analytics
            │
            ▼
SQLite Database
├── Vehicles
├── Distances
└── Transporters
            │
            ▼
Gemini AI Layer
            │
            ▼
Recommendations & Explanations
```

---

## Technology Stack

* Python
* Streamlit
* SQLite
* Google Gemini API
* Pandas

---

## Database Design

The system utilizes a relational SQLite database consisting of:

### Vehicles Table

Stores vehicle specifications including:

* Vehicle category
* Capacity
* Axles
* ODC eligibility

### Distances Table

Stores route information including:

* Origin
* Destination
* Distance
* Route details

### Transporters Table

Stores transporter information including:

* Transporter name
* Category
* MSME status
* Approval details

---

## Project Objectives

* Automate logistics planning activities
* Recommend suitable transportation resources
* Identify ODC shipment requirements
* Support route planning decisions
* Generate packaging recommendations
* Provide AI-powered logistics assistance
* Reduce manual effort in logistics operations

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/ai-logistics-planning-system.git
cd ai-logistics-planning-system
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux / Mac

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run Homepage.py
```

---

## Future Enhancements

* PostgreSQL/MySQL integration
* Real-time shipment tracking
* Advanced route optimization
* Transporter recommendation engine
* Predictive logistics analytics
* Role-based access control
* Automated logistics report generation

---

## Author

**Shruti Prasad**
B.Tech Artificial Intelligence and Data Science Engineering
Specialization: Transportation and Logistics
Gati Shakti Vishwavidyalaya

---

## Disclaimer

This project was developed as part of an internship and is intended for educational and demonstration purposes. Any company-specific operational data has been excluded from the public version of the project.
