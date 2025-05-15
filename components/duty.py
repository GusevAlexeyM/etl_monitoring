import streamlit as st
from datetime import datetime
from utils.helpers import fetch_data

def render():
    st.header("👨‍💼 Дежурные")

    users = fetch_data("users")
    groups = fetch_data("support_groups")

    week = st.number_input("Введите номер недели", min_value=1, max_value=52, value=datetime.now().isocalendar()[1])
    st.subheader(f"Дежурные на неделю {week}")

    for group in groups:
        group_users = [u for u in users if u.get("support_group_id") == group["id"]]
        if group_users:
            index = week % len(group_users)
            duty_user = group_users[index]

            st.markdown(
                f"""
                <div style="background-color:#1a1a1a; padding:16px 20px; border-radius:10px; margin-bottom:12px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); color:#e0e0e0; font-size:1.1em;">
                    <strong>{group['name']}</strong><br>
                    <span style="color:#bbb; font-size: 0.95em;">Дежурный: {duty_user['username']} ({duty_user['email']})</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"**{group['name']}**: Нет участников в группе.")
