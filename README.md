# NHS Diabetes Analytics & Clinical Decision Support System

## Executive Summary
An end-to-end Health Informatics data pipeline designed to ingest, process, and analyze 100,000 patient records. This system normalizes raw clinical data into a T-SQL relational database, applies statistical risk models using Python, and delivers interactive executive dashboards in Power BI to support NHS clinical decision-making and resource allocation.

---

## System Architecture & Tech Stack
* **Database Engine:** Microsoft SQL Server Management Studio (SSMS)
* **Query Language:** T-SQL (DDL/DML, Schema Normalization, Relational Integrity)
* **Data Engineering & Scripting:** Python (`pandas`, `pyodbc`, `sqlalchemy`)
* **Business Intelligence:** Power BI Desktop (DAX, Data Modeling, Operational Reporting)
* **Governance & Standards:** Data Anonymization, NHS Information Governance Principles

---

## Implementation Roadmap & Milestones

### **Phase 1: Relational Database Architecture (SSMS & T-SQL)**
- [x] **Milestone 1.1: Database Initialization & Relational Schema Design**
  * Initialized `Diabetes_AnalyticsDB`.
  * Normalized flat dataset into 1-to-Many relational structure (`Patients` and `ClinicalMetrics`).
  * Defined strict data typing (`FLOAT` for decimal ages/BMI, `BIT` flags for clinical indicators) and relational key constraints.
  * *Artifact:* [`01_create_schema.sql`](./01_create_schema.sql)
     
