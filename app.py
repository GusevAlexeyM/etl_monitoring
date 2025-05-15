import streamlit as st
from auth import login
from components import home, duty, dag, jobs, users, support

st.set_page_config(page_title="Мониторинг ETL-процессов", layout="wide")

# Авторизация
if "user" not in st.session_state:
    login()
    st.stop()

# --- Боковая панель: карточка пользователя ---
if "user" in st.session_state:
    user = st.session_state["user"]
    st.sidebar.markdown(
        f'''
        <div style="background-color: #262730; padding: 12px 14px; border-radius: 8px; margin-top: 10px;
                    display: flex; align-items: center; color: #ffffff;">
            <div style="font-size: 22px; margin-right: 10px;">👤</div>
            <div style="line-height: 1.2;">
                <div style="font-weight: 600;">{user['username']}</div>
                <div style="font-size: 12px; color: #cccccc;">{user['email']}</div>
                <div style="font-size: 12px; color: #888888;">Роль: {user['role']}</div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# --- Навигация ---
st.sidebar.title("🔍 Навигация")

if "page" not in st.session_state:
    st.session_state.page = "Главная"

if st.sidebar.button("🏠 Главная"):
    st.session_state.page = "Главная"
if st.sidebar.button("👨‍💼 Дежурные"):
    st.session_state.page = "Дежурные"
if st.sidebar.button("📊 DAG"):
    st.session_state.page = "DAG"
if st.sidebar.button("📈 Jobs"):
    st.session_state.page = "Jobs"
if st.sidebar.button("👥 Пользователи"):
    st.session_state.page = "Пользователи"
if st.sidebar.button("👨‍🔧 Группы поддержки"):
    st.session_state.page = "Группы поддержки"

# --- Кнопка выхода (внизу) ---
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Выйти"):
    st.session_state.clear()
    st.rerun()

# --- Контент текущей страницы ---
if st.session_state.page == "Главная":
    home.render()
elif st.session_state.page == "Дежурные":
    duty.render()
elif st.session_state.page == "DAG":
    dag.render()
elif st.session_state.page == "Jobs":
    jobs.render()
elif st.session_state.page == "Пользователи":
    users.render()
elif st.session_state.page == "Группы поддержки":
    support.render()
