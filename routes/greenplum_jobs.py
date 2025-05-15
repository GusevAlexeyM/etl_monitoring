from fastapi import APIRouter
from database import get_db_connection

router = APIRouter()

@router.get("/")
def get_greenplum_jobs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, owner_id, support_group_id FROM greenplum_jobs;")
    jobs = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "owner_id": row[3],
            "support_group_id": row[4]
        }
        for row in jobs
    ]