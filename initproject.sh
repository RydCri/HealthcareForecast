#!/bin/bash
# Shell script example for making your own mock ETL project
# chmod +x initproject.sh
# ./initproject.sh

mkdir -p hospital-forecasting/{data/{admissions,procedures,staffing,occupancy},dags,dbt/{models/{staging,marts,snapshots},seeds},notebooks/{eda,forecasting,cost_prediction,classification},src/{data_gen,etl,utils,config},streamlit_app/{pages,components},api/{routes,models},tests}

touch hospital-forecasting/{.env,requirements.txt,pyproject.toml,README.md}
touch hospital-forecasting/dbt/dbt_project.yml
touch hospital-forecasting/streamlit_app/app.py
touch hospital-forecasting/api/main.py

# Example files to get started
touch hospital-forecasting/src/data_gen/generate_admissions.py
touch hospital-forecasting/dags/ingest_to_gcs.py
touch hospital-forecasting/dags/load_to_bigquery.py
touch hospital-forecasting/tests/test_data_gen.py
