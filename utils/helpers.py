import requests
import streamlit as st
import pandas as pd
from datetime import datetime


def fetch_data(endpoint, api_url="http://127.0.0.1:8000"):
    try:
        response = requests.get(f"{api_url}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except Exception as e:
        st.error(f"Ошибка при получении данных: {e}")
        return []


def get_owner_name(owner_id):
    users = fetch_data("users")
    for u in users:
        if u["id"] == owner_id:
            return u["username"]
    return "—"


def get_support_group_name(group_id):
    groups = fetch_data("support_groups")
    for g in groups:
        if g["id"] == group_id:
            return g["name"]
    return "—"


def get_duty_contact(group_id):
    users = fetch_data("users")
    current_week = datetime.now().isocalendar()[1]
    group_users = [u for u in users if u.get("support_group_id") == group_id]
    if not group_users:
        return "Нет дежурного"
    index = current_week % len(group_users)
    u = group_users[index]
    return f"{u['username']} ({u['email']})"
