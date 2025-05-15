import streamlit as st
import pandas as pd
from utils.helpers import fetch_data, get_owner_name, get_support_group_name

def render():
    st.header("👥 Пользователи")
    users = fetch_data("users")
    jobs = fetch_data("greenplum_jobs")
    dags = fetch_data("airflow_assets")
    groups = fetch_data("support_groups")

    name_dict = {f"{u['username']} ({u['email']})": u for u in users}
    selected_label = st.selectbox("Выберите пользователя", list(name_dict.keys()))
    user = name_dict[selected_label]
    group = next((g["name"] for g in groups if g["id"] == user["support_group_id"]), "—")

    st.markdown(f"**Группа поддержки:** {group}")

    st.subheader("Активы Greenplum")
    user_jobs = [j for j in jobs if j["owner_id"] == user["id"]]
    for j in user_jobs:
        j["owner"] = get_owner_name(j["owner_id"])
        j["support_group"] = get_support_group_name(j["support_group_id"])
    st.dataframe(pd.DataFrame(user_jobs)[["name", "description", "owner", "support_group"]])

    st.subheader("Активы Airflow")
    user_dags = [d for d in dags if d["owner_id"] == user["id"]]
    for d in user_dags:
        d["owner"] = get_owner_name(d["owner_id"])
        d["support_group"] = get_support_group_name(d["support_group_id"])
    st.dataframe(pd.DataFrame(user_dags)[["name", "description", "owner", "support_group"]])