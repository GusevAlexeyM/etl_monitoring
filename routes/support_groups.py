from fastapi import APIRouter
from database import get_db_connection

router = APIRouter()

@router.get("/")
def get_support_groups():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM support_groups;")
    groups = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in groups
    ]