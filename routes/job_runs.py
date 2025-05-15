from fastapi import APIRouter
from database import get_db_connection

router = APIRouter()

@router.get("/")
def get_job_runs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, greenplum_job_id, status, start_time, end_time FROM job_runs;")
    runs = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "greenplum_job_id": row[1],
            "status": row[2],
            "start_time": row[3],
            "end_time": row[4]
        }
        for row in runs
    ]