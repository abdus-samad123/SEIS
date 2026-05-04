import streamlit as st
import pandas as pd
import plotly.express as px
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# =========================
# LOAD DATA (FIXED PATH)
# =========================
file_path = os.path.join("data", "student_data.csv")
df = pd.read_csv(file_path)

st.set_page_config(page_title="Student Dashboard", layout="wide")

# =========================
# LOGIN SYSTEM
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if email == "admin@gmail.com" and password == "1234":
        st.session_state.logged_in = True
    else:
        st.error("Invalid credentials")

def logout():
    st.session_state.logged_in = False

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.logged_in:
    st.title("🔐 Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login()

    st.stop()

# =========================
# DASHBOARD TITLE
# =========================
st.title("📊 Student Engagement Intelligence Dashboard")

# Logout button
if st.button("Logout"):
    logout()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔍 Filters")

dept = st.sidebar.multiselect("Department", df["Department"].unique())
tier = st.sidebar.multiselect("College Tier", df["College_Tier"].unique())

filtered_df = df.copy()

if dept:
    filtered_df = filtered_df[filtered_df["Department"].isin(dept)]

if tier:
    filtered_df = filtered_df[filtered_df["College_Tier"].isin(tier)]

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Students", len(filtered_df))
col2.metric("Placement Rate", round(filtered_df['Placement_Status'].mean()*100, 2))
col3.metric("Avg CGPA", round(filtered_df['CGPA'].mean(), 2))

st.divider()

# =========================
# CHARTS
# =========================

# Attendance vs Placement
st.subheader("📌 Attendance vs Placement")
fig1 = px.scatter(filtered_df, x="Attendance_%", y="Placement_Status")
st.plotly_chart(fig1, use_container_width=True)

# Login Frequency
st.subheader("📌 Login Frequency vs Placement")
fig2 = px.box(filtered_df, x="Login_Frequency", y="Placement_Status")
st.plotly_chart(fig2, use_container_width=True)

# Time Spent
st.subheader("📌 Time Spent vs Outcome")
fig3 = px.scatter(filtered_df, x="Time_Spent_Hours", y="Placement_Status")
st.plotly_chart(fig3, use_container_width=True)

# Quiz Score
st.subheader("📌 Quiz Score vs Placement")
fig4 = px.histogram(filtered_df, x="Quiz_Score", color="Placement_Status")
st.plotly_chart(fig4, use_container_width=True)

# Doubts
st.subheader("📌 Doubts Raised vs Placement")
fig5 = px.scatter(filtered_df, x="Doubts_Raised", y="Placement_Status")
st.plotly_chart(fig5, use_container_width=True)

# Hackathons
st.subheader("📌 Hackathons vs Placement")
fig6 = px.scatter(filtered_df, x="Hackathons", y="Placement_Status")
st.plotly_chart(fig6, use_container_width=True)

# =========================
# DOWNLOAD BUTTON
# =========================
st.subheader("📥 Download Filtered Report")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name='student_report.csv',
    mime='text/csv',
)

# =========================
# ML MODEL
# =========================
st.subheader("🤖 Placement Prediction Model")

# Prepare data
df_model = df.select_dtypes(include=['int64', 'float64']).dropna()

X = df_model.drop("Placement_Status", axis=1)
y = df_model["Placement_Status"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

st.metric("Model Accuracy", round(acc * 100, 2))

# =========================
# PREDICTION UI
# =========================
st.subheader("🎯 Predict Placement")

input_data = {}

for col in X.columns:
    input_data[col] = st.number_input(
        f"{col}",
        float(df[col].min()),
        float(df[col].max())
    )

if st.button("Predict"):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]

    if prediction == 1:
        st.success("✅ Likely to be Placed")
    else:
        st.error("❌ Not Likely to be Placed")
