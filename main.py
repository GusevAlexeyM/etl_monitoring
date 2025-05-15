from fastapi import FastAPI
from routes import (
    airflow_assets,
    greenplum_jobs,
    dag_runs,
    job_runs,
    failures,
    support_groups,
    rou_users
)

app = FastAPI(title="ETL Monitoring API")

# Подключение всех роутов
app.include_router(airflow_assets.router, prefix="/airflow_assets", tags=["Airflow Assets"])
app.include_router(greenplum_jobs.router, prefix="/greenplum_jobs", tags=["Greenplum Jobs"])
app.include_router(dag_runs.router, prefix="/dag_runs", tags=["DAG Runs"])
app.include_router(job_runs.router, prefix="/job_runs", tags=["Job Runs"])
app.include_router(failures.router, prefix="/failures", tags=["Failures"])
app.include_router(support_groups.router, prefix="/support_groups", tags=["Support Groups"])
app.include_router(rou_users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "ETL Monitoring API is running!"}