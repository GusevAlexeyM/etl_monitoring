from fastapi import APIRouter
from database import get_db_connection

router = APIRouter()

@router.get("/")
def get_dag_runs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, airflow_asset_id, status, start_time, end_time FROM dag_runs;")
    runs = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "airflow_asset_id": row[1],
            "status": row[2],
            "start_time": row[3],
            "end_time": row[4]
        }
        for row in runs
    ]