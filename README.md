# Ecommerce ETL Pipeline using Airflow & dbt

## Project Overview
This project implements an **end-to-end Ecommerce ETL pipeline** using **Apache Airflow**, **PostgreSQL**, **dbt**, **MinIO (S3)**, and **Docker**.

The pipeline extracts data from multiple sources, stages it in a data warehouse, transforms it into a **star schema** using dbt, and applies **data quality tests** to ensure reliability.

---

## Architecture

### Data Sources
- **PostgreSQL (Source DB)**  
  - Tables: `users`, `products`
- **REST API (Mock API)**  
  - Endpoint: `/orders` (paginated)
- **S3 (MinIO)**  
  - File: `inventory.csv`

### Data Warehouse
- **PostgreSQL**
  - Staging tables: `stg_users`, `stg_products`, `stg_orders`, `stg_inventory`
  - Final models:
    - `dim_users`
    - `dim_products`
    - `fct_orders` (incremental)

---

##  ETL Workflow (Airflow DAG)

**DAG Name:** `ecommerce_etl_pipeline`

### Steps:
1. **Extract (Parallel Tasks)**
   - Extract users & products from PostgreSQL
   - Extract orders from REST API
   - Extract inventory data from S3 (MinIO)

2. **Load**
   - Load raw data into warehouse staging tables

3. **Transform**
   - Run `dbt run` to create dimension and fact tables

4. **Data Quality**
   - Run `dbt test` with `unique` and `not_null` checks

---

##  dbt Models

### Star Schema

#### Dimension Tables
- `dim_users`
- `dim_products`

#### Fact Table
- `fct_orders`
  - Incremental model
  - Uses `order_id` as unique key

### Tests
- `unique`
- `not_null`

Applied on primary keys of all final models.

---

## Project Structure

```text
airflow-data-pipeline/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .gitignore
├── README.md
│
├── dags/
│   └── ecommerce_etl_pipeline.py
│
├── dbt_project/
│   └── ecommerce_dbt/
│       ├── dbt_project.yml
│       ├── profiles.yml
│       ├── models/
│       │   ├── staging/
│       │   └── marts/
│       └── tests/
│
├── seeds/
│   ├── source_db/
│   │   └── init.sql
│   └── s3_data/
│       └── inventory.csv
│
├── mock_api/
│   ├── app.py
│   └── Dockerfile
│
└── logs/
```
### How to Run the Project
**1.Start all services:**
```
docker compose up -d
```
**2.Access Airflow UI:**
- URL: http://localhost:8085
- Username: admin
- Password: admin

**3.Trigger DAG:**
- Enable ecommerce_etl_pipeline
- Click ▶️ Trigger DAG

---
### Verify Data in Warehouse
```
docker exec -it data_warehouse psql -U user -d dwh
SELECT * FROM dim_users;
SELECT * FROM dim_products;
SELECT * FROM fct_orders;
```
**Author:**
Sanjana Medapati
