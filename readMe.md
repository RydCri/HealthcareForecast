### Hospital Resource & Cost Forecasting Platform
<br>
This project simulates how a hospital might use data engineering and ETL pipelines to manage cost forecasts, explore coefficients through data science and handle department queries.
<hr>
Objective:
Forecast hospital resource demand (beds, ICU units, staff) and patient cost using historical data. Provide analytics dashboards and ML-driven insights for hospital administrators.

        ┌──────────────┐         ┌────────────────┐
        │  Data Gen /  │ ─────▶ │ Raw GCS Bucket │
        │  Ingestion   │         └────────────────┘
        └────┬─────────┘
             ▼
     ┌─────────────────┐        ┌──────────────┐
     │ Kafka / PubSub  │ ─────▶ │  BigQuery     │ ◀────┐
     └─────────────────┘        └────┬──────────┘      │
                                     ▼                 ▼
                               ┌──────────────┐   ┌────────────┐
                               │   dbt        │   │ Jupyter DS │
                               │ Transform    │   │ Notebooks  │
                               └────┬─────────┘   └────┬───────┘
                                    ▼                  ▼
                            ┌────────────────┐   ┌───────────────┐
                            │ Dash / Streamlit│ ◀▶│ REST API (Flask)│
                            │ Admin Dashboard │   └───────────────┘
                            └────────────────┘

<hr>
Data Simulation 
<br>
This project simulates the following datasets:

1. Patient Admission Events (Daily)

        | patient_id | admit_date |	dept | severity | diagnosis | age |	insurance_type |
 

2. Procedures / Billing Records

        | procedure_id | patient_id | procedure | cost | performed_by | date |

3. Staffing Schedule
   
         | staff_id | role | department | shift_date | hours |

4. Bed /  ICU Occupancy
   
         | bed_id | dept | patient_id | start_time | end_time | is_ICU |

<hr>

## Setup

1. Create a virtual environment and Install requirements.

         python -m venv <your_environment_name>
         pip install -r requirements.txt
2. Docker setup

   I composed in my IDE's local terminal with my container running on Docker Desktop. Adjust how this suits you best.
         
         docker compose up airflow-init

   Wait for this to finish. Then:

         docker compose up
3. Access Apache Airflow

   After your container is running: The Admin Portal is ran through Airflow, accessible on localhost:8080. User: admin, Password: admin. 
<br>
   <img alt="Apache Airflow Admin Login" height="300" src="airflow_screen.png" width="400"/>
