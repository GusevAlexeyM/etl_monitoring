import streamlit as st
import bcrypt
from database import get_db_connection


def login():
    st.title("🔐 Вход в систему")

    email = st.text_input("Email").strip().lower()
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT id, username, email, password_hash, role, support_group_id FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

            if user and bcrypt.checkpw(password.encode(), user[3].encode()):
                # Успешный вход — сохраняем данные пользователя
                st.session_state.user = {
                    "id": user[0],
                    "username": user[1],
                    "email": user[2],
                    "role": user[4],
                    "support_group_id": user[5]
                }
                st.success("Успешный вход!")
                st.rerun()
            else:
                st.error("Неверный email или пароль")

        except Exception as e:
            st.error(f"Ошибка подключения к базе данных: {e}")
        finally:
            if conn:
                conn.close()
