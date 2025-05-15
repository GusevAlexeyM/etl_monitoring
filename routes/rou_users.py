from fastapi import APIRouter
from database import get_db_connection

router = APIRouter()

@router.get("/")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, email, role, support_group_id, created_at FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "role": row[3],
            "support_group_id": row[4],
            "created_at": row[5]
        }
        for row in users
    ]