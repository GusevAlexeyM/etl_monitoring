import streamlit as st
import pandas as pd
from utils.helpers import fetch_data, get_owner_name, get_support_group_name, get_duty_contact
import altair as alt
from pandas.api.types import CategoricalDtype

def plot_status_chart(df, failures, asset_name, owner_id, support_group_id):
    if df.empty:
        st.info("Нет данных для построения графика.")
        return

    status_labels = {-1: "Упал в ошибку", 1: "Готов к запуску", 2: "Выполняется", 3: "Выполнено"}
    status_order = ["Упал в ошибку", "Готов к запуску", "Выполняется", "Выполнено"]

    df["status_text"] = df["status"].map(status_labels)
    df["status_text"] = df["status_text"].astype(CategoricalDtype(categories=status_order, ordered=True))
    df["start_time"] = pd.to_datetime(df["start_time"])

    base_chart = (
        alt.Chart(df)
        .mark_line(point=True, strokeWidth=3, color="#0077b6")
        .encode(
            x=alt.X("start_time:T", title="Дата и время", axis=alt.Axis(format="%d.%m %H:%M", tickMinStep=7200000)),
            y=alt.Y("status_text:N", title="Статус", sort=status_order),
            tooltip=["start_time:T", "status_text"]
        )
    )

    if failures:
        df_fail = pd.DataFrame(failures)
        if not df_fail.empty and "occurred_at" in df_fail.columns:
            df_fail["occurred_at"] = pd.to_datetime(df_fail["occurred_at"])
            df_fail["status_text"] = "Упал в ошибку"

            error_layer = (
                alt.Chart(df_fail)
                .mark_circle(size=100, color="red")
                .encode(
                    x="occurred_at:T",
                    y=alt.Y("status_text:N", sort=status_order),
                    tooltip=["occurred_at:T", "error_message"]
                )
            )
            chart = base_chart + error_layer
        else:
            chart = base_chart
    else:
        chart = base_chart

    st.altair_chart(chart, use_container_width=True)

    # Информация об активе
    st.subheader("ℹ️ Информация о DAG")
    st.markdown(f"**Название:** {asset_name}")
    st.markdown(f"**Владелец:** {get_owner_name(owner_id)}")
    st.markdown(f"**Группа поддержки:** {get_support_group_name(support_group_id)}")

    if failures:
        df_failures = pd.DataFrame(failures)
        if not df_failures.empty and "occurred_at" in df_failures.columns:
            last_failure = df_failures.sort_values("occurred_at", ascending=False).iloc[0]
            error_id = last_failure.get("dag_run_id", "—")
            st.error(f"❌ Последняя ошибка (ID {error_id}): {last_failure.get('error_message', '—')}")
            st.warning(f"📩 Дежурный по группе: {get_duty_contact(support_group_id)}")

def render():
    st.header("📊 DAG")

    dags = fetch_data("airflow_assets")
    dag_runs = fetch_data("dag_runs")
    failures = fetch_data("failures")

    if not dags:
        st.warning("Нет данных DAG.")
        return

    dag_names = {d["id"]: d["name"] for d in dags}
    if not dag_names:
        st.warning("Нет доступных DAG для выбора.")
        return

    selected_id = st.selectbox("Выберите DAG", list(dag_names.keys()), format_func=lambda x: dag_names.get(x, "—"))

    runs = [r for r in dag_runs if r.get("airflow_asset_id") == selected_id]
    if not runs:
        st.info("Нет запусков для выбранного DAG.")
        return

    run_ids = [r["id"] for r in runs]
    fails = [f for f in failures if f.get("dag_run_id") in run_ids]

    asset = next((d for d in dags if d["id"] == selected_id), {})
    owner_id = asset.get("owner_id")
    group_id = asset.get("support_group_id")

    df_runs = pd.DataFrame(runs)
    if df_runs.empty or "status" not in df_runs.columns or "start_time" not in df_runs.columns:
        st.info("Недостаточно данных для отображения.")
        return

    st.dataframe(df_runs)
    plot_status_chart(df_runs, fails, asset.get("name", "—"), owner_id, group_id)
