from fastapi import APIRouter
from database import get_db_connection

router = APIRouter()

@router.get("/")
def get_failures():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, job_run_id, dag_run_id, error_message, occurred_at FROM failures;")
    failures = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "job_run_id": row[1],
            "dag_run_id": row[2],
            "error_message": row[3],
            "occurred_at": row[4]
        }
        for row in failures
    ]