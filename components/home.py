import streamlit as st
import pandas as pd
from utils.helpers import fetch_data, get_owner_name, get_support_group_name

def render():
    st.header("🏠 Все активы")

    assets = fetch_data("airflow_assets")
    jobs = fetch_data("greenplum_jobs")
    runs_dag = fetch_data("dag_runs")
    runs_job = fetch_data("job_runs")

    STATUS_COLORS = {-1: "🔴", 1: "🔵", 2: "🟡", 3: "🟢"}

    def last_status_dots(runs, asset_id_field, asset_id):
        relevant = [r["status"] for r in runs if r[asset_id_field] == asset_id]
        relevant = relevant[-3:] if relevant else []
        return " ".join(STATUS_COLORS.get(s, "⚪") for s in relevant)

    st.subheader("DAG")
    df_dag = pd.DataFrame(assets)
    if not df_dag.empty:
        df_dag["Владелец"] = df_dag["owner_id"].apply(get_owner_name)
        df_dag["Группа поддержки"] = df_dag["support_group_id"].apply(get_support_group_name)
        df_dag["Статусы"] = df_dag["id"].apply(lambda i: last_status_dots(runs_dag, "airflow_asset_id", i))
        st.dataframe(df_dag[["name", "description", "Владелец", "Группа поддержки", "Статусы"]])

    st.subheader("Jobs")
    df_job = pd.DataFrame(jobs)
    if not df_job.empty:
        df_job["Владелец"] = df_job["owner_id"].apply(get_owner_name)
        df_job["Группа поддержки"] = df_job["support_group_id"].apply(get_support_group_name)
        df_job["Статусы"] = df_job["id"].apply(lambda i: last_status_dots(runs_job, "greenplum_job_id", i))
        st.dataframe(df_job[["name", "description", "Владелец", "Группа поддержки", "Статусы"]])

    st.caption("🔴 — Упал в ошибку | 🔵 — Готов к запуску | 🟡 — Выполняется | 🟢 — Выполнено")