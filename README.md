# FreightIQ - AI Logistics Planning & Recommendation System

## Overview

FreightIQ is an AI-powered Logistics Planning and Recommendation System developed to assist logistics planners in making informed transportation decisions. The platform combines logistics databases, rule-based recommendation engines, route intelligence, packaging planning, dashboard analytics, and AI-powered explanations into a unified decision-support system.

The application helps users evaluate shipment requirements based on cargo weight, dimensions, route information, transporter availability, and packaging constraints while generating intelligent logistics recommendations.

---

## Problem Statement

Logistics planning often involves analyzing multiple datasets, vehicle specifications, route information, transporter details, and cargo requirements before selecting a suitable transportation solution. Manual evaluation can be time-consuming and prone to inconsistencies.

FreightIQ addresses this challenge by integrating logistics data, recommendation engines, and AI-powered assistance into a single platform that supports faster and more informed decision-making.

---

## Key Features

* Logistics Dashboard
* Vehicle Recommendation Engine
* ODC Assessment Engine
* Route Intelligence Engine
* Packaging Planning Assistant
* AI Logistics Assistant
* Database Lookup Center
* AI-Powered Recommendation Explanations

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
├── Packaging Planning Assistant
└── Dashboard Analytics
            │
            ▼
SQLite Database
├── Vehicles
├── Distances
└── Transporters
            │
            ▼
Gemini AI
            │
            ▼
Recommendations & Explanations
```

---

## Why RAG Was Not Used

Retrieval-Augmented Generation (RAG) is generally useful when information is stored in large collections of unstructured documents such as PDFs, reports, manuals, or knowledge bases.

In this project, the required information is already available in structured relational database tables. Vehicle specifications, route distances, transporter details, and logistics constraints can be retrieved directly through database queries and recommendation engines.

Instead of using a vector database and document retrieval pipeline, the system directly accesses structured logistics data and uses Gemini AI to generate explanations and recommendations.

Benefits of this approach include:

* Faster response times
* Reduced infrastructure complexity
* Accurate retrieval of structured logistics information
* Reliable rule-based calculations
* Lower operational overhead

---

## Technology Stack

* Python
* Streamlit
* SQLite
* Pandas
* Google Gemini API

---

## Future Enhancements

* PostgreSQL or MySQL integration
* Real-time shipment tracking
* Advanced route optimization
* Predictive logistics analytics
* Transporter recommendation engine
* Automated logistics report generation
* Role-based access control

---

## Academic Context

This project was developed during a Summer Internship at Bharat Heavy Electricals Limited (BHEL), Haridwar.

Program:
B.Tech Artificial Intelligence and Data Science Engineering

Specialization:
Transportation and Logistics

Institution:
Gati Shakti Vishwavidyalaya

---

## Author

Shruti Prasad

---

## Disclaimer

This repository contains a demonstration version of the project. Company-specific operational data and confidential information have been excluded from the public release.
