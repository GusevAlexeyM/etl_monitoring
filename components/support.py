import streamlit as st
from utils.helpers import fetch_data

def render():
    st.header("👨‍🔧 Группы поддержки")

    groups = fetch_data("support_groups")
    users = fetch_data("users")
    airflow_assets = fetch_data("airflow_assets")
    greenplum_jobs = fetch_data("greenplum_jobs")

    for group in groups:
        st.markdown(f"### 🛠️ {group['name']}")

        group_users = [user for user in users if user["support_group_id"] == group["id"]]
        group_airflow_assets = [a for a in airflow_assets if a["support_group_id"] == group["id"]]
        group_gp_jobs = [j for j in greenplum_jobs if j["support_group_id"] == group["id"]]

        if group_users:
            st.markdown("#### 👥 Участники группы:")
            cols = st.columns(2)
            for idx, user in enumerate(group_users):
                with cols[idx % 2]:
                    st.markdown(
                        f'''
                        <div style="background-color:#1e1e1e; padding: 15px; border-radius: 10px;
                                    margin-bottom: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);">
                            <p style="color:#ffffff; font-size:16px; margin:0;"><strong>👤 {user['username']}</strong></p>
                            <p style="color:#aaaaaa; font-size:14px; margin:5px 0 0;">📧 {user['email']}</p>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
        else:
            st.markdown("_Нет участников в этой группе._")

        st.markdown("#### 📊 DAG'и Airflow:")
        if group_airflow_assets:
            cols = st.columns(2)
            for idx, asset in enumerate(group_airflow_assets):
                with cols[idx % 2]:
                    st.markdown(
                        f'''
                        <div style="background-color:#2a2a2a; padding: 15px; border-radius: 10px;
                                    margin-bottom: 10px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);">
                            <p style="color:#33ccff; font-size:15px; margin:0;"><strong>{asset['name']}</strong></p>
                            <p style="color:#cccccc; font-size:14px; margin:5px 0 0;">{asset['description']}</p>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
        else:
            st.markdown("_Нет DAG'ов на поддержке._")

        st.markdown("#### 📈 Job'ы Greenplum:")
        if group_gp_jobs:
            cols = st.columns(2)
            for idx, job in enumerate(group_gp_jobs):
                with cols[idx % 2]:
                    st.markdown(
                        f'''
                        <div style="background-color:#2a2a2a; padding: 15px; border-radius: 10px;
                                    margin-bottom: 10px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);">
                            <p style="color:#ffcc66; font-size:15px; margin:0;"><strong>{job['name']}</strong></p>
                            <p style="color:#cccccc; font-size:14px; margin:5px 0 0;">{job['description']}</p>
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )
        else:
            st.markdown("_Нет джобов на поддержке._")

        st.markdown("---")