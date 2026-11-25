# Telecom Customer Intelligence Platform

An end-to-end Data Science project focused on customer
churn prediction, customer segmentation, and personalized
Next Best Offer recommendations in the telecom industry.

## Project Objectives

- Build a reliable customer data pipeline.
- Analyze customer behavior and churn drivers.
- Develop and evaluate machine learning models.
- Segment customers based on their characteristics.
- Prototype personalized retention recommendations.
- Evaluate potential business impact.

## Technology Stack

Python, SQL, PostgreSQL, Pandas, Scikit-learn,
CatBoost, FastAPI, Streamlit, Docker.

## Dataset

IBM Telco Customer Churn Dataset.

## Project Status

In Development

## Data Architecture

The project implements a three-layer data architecture:

- Bronze (raw): original customer data.
- Silver (staging): cleaned and validated customer data.
- Gold (analytics): business-ready SQL views.

## Data Quality

- Missing value handling
- Duplicate detection
- Data type conversion
- Schema validation
- Business rule validation
- Record count verification
- Automated unit tests