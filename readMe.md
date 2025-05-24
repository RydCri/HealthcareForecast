### Hospital Resource & Cost Forecasting Platform
<br>
This project simulates how a hospital might use data engineering and ETL pipelines to manage cost forecasts, explore coefficients through data science and handle department queries.
<hr>
Objective:
Forecast hospital resource demand (beds, ICU units, staff) and patient cost using historical data. Provide analytics dashboards and ML-driven insights for hospital administrators.
<hr>

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
                            │ Dash / Airflow │ ◀▶│ REST API (Flask)│
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

## Usage (WIP)

<i>A Demo of this project will be hosted in the future.</i>
<br>

1. Access Apache Airflow
<br>
The Admin Portal is ran through Airflow, User: admin, Password: admin.
<br>
<img style="width:300px; height:220px;" alt="Apache Airflow Admin Login" src="airflow_screen.png"/>


2. Verify DAGs
<br>
Once logged in, you should see your DAGs under the DAGs tab.
<br>
<img style="height:220px;" alt="Airflow DAG dashboard" src="airflow-dashboard.png"/>

3. Trigger a DAG
<br>
From the Airflow UI, click on a DAG and manually trigger it to start the workflow.
<hr>

## DAGs and Workflow

<div>
<h3>This dashboard simulates a workspace that receives a daily and weekly reports to our mock hospital.</h3>
<ul>
<li>
<h4>generate_admission_dag</h4> 
<span>Generates 1000 patients admitted to the hospital, running this DAG creates a .csv of this admission data every 24 hours.</span>
<p>Randomized categorical data is generated for the following patient fields: patient_id, admit_date, dept, severity, diagnosis, age, insurance_type</p>
<p>Daily files are uploaded to a GCS bucket.</p>
</li>
<li>
<h4>ingest_admission_dag</h4>
<span>Receives .csv files from Google Cloud </span>
<p>Files output by generate_admission_dag are meant to be held in GCS to simulate reports sent by an admissions department.</p>
<p>This DAG downloads these files stored in an online GCS bucket. Locally stored in /opt/airflow/data/admissions/</p>
</li>

</ul>
</div>




[//]: # (TODO: explain schedular and other dags)
