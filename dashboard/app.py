import streamlit as st
import pandas as pd
import plotly.express as px

# LOAD DATA
df = pd.read_csv("../data/student_data.csv")

st.set_page_config(page_title="Student Dashboard", layout="wide")

# LOGIN SYSTEM (FRONTEND SIMULATION)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if email == "admin@gmail.com" and password == "1234":
        st.session_state.logged_in = True
    else:
        st.error("Invalid credentials")

def logout():
    st.session_state.logged_in = False

# LOGIN PAGE
if not st.session_state.logged_in:
    st.title("🔐 Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login()

    st.stop()

# DASHBOARD
st.title("📊 Student Engagement Intelligence Dashboard")

# LOGOUT BUTTON
if st.button("Logout"):
    logout()

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Students", len(df))
col2.metric("Placement Rate", round(df['Placement_Status'].mean()*100, 2))
col3.metric("Avg CGPA", round(df['CGPA'].mean(), 2))

st.divider()

# 1. ATTENDANCE vs PLACEMENT
st.subheader("📌 Attendance vs Placement")

fig1 = px.scatter(df, x="Attendance_%", y="Placement_Status",
                  title="Attendance Impact on Placement")

st.plotly_chart(fig1, use_container_width=True)

# 2. LOGIN FREQUENCY
st.subheader("📌 Login Frequency vs Placement")

fig2 = px.box(df, x="Login_Frequency", y="Placement_Status")

st.plotly_chart(fig2, use_container_width=True)

# 3. TIME SPENT
st.subheader("📌 Time Spent vs Outcome")

fig3 = px.scatter(df, x="Time_Spent_Hours", y="Placement_Status")

st.plotly_chart(fig3, use_container_width=True)

# 4. QUIZ PERFORMANCE
st.subheader("📌 Quiz Score vs Placement")

fig4 = px.histogram(df, x="Quiz_Score", color="Placement_Status")

st.plotly_chart(fig4, use_container_width=True)

# 5. DOUBTS ANALYSIS
st.subheader("📌 Doubts Raised vs Placement")

fig5 = px.scatter(df, x="Doubts_Raised", y="Placement_Status")

st.plotly_chart(fig5, use_container_width=True)

# 6. EVENTS IMPACT
st.subheader("📌 Hackathons vs Placement")

fig6 = px.scatter(df, x="Hackathons", y="Placement_Status")

st.plotly_chart(fig6, use_container_width=True)
