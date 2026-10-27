from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analysis import (
    get_overview_stats,
    get_top_relationships,
    summarize_attendance_groups,
    summarize_by_major,
    summarize_by_year,
)
from src.data_cleaning import prepare_data

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_students.csv"


@st.cache_data
def load_dashboard_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        prepare_data()
    return pd.read_csv(DATA_PATH)


def run_dashboard() -> None:
    st.set_page_config(
        page_title="Campus Student Success Dashboard",
        page_icon="🎓",
        layout="wide",
    )

    df = load_dashboard_data()
    overview = get_overview_stats(df)

    st.title("🎓 Campus Student Success Dashboard")
    st.caption("Exploring patterns between academic performance, study habits, attendance, and student characteristics.")

    st.sidebar.header("Filters")
    selected_year = st.sidebar.multiselect("Academic Year", options=sorted(df["academic_year"].unique().tolist()))
    selected_major = st.sidebar.multiselect("Major", options=sorted(df["major"].unique().tolist()))
    selected_gender = st.sidebar.multiselect("Gender", options=sorted(df["gender"].unique().tolist()))

    if selected_year:
        df = df[df["academic_year"].isin(selected_year)]
    if selected_major:
        df = df[df["major"].isin(selected_major)]
    if selected_gender:
        df = df[df["gender"].isin(selected_gender)]

    st.subheader("Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", f"{overview['total_students']:,}")
    col2.metric("Average GPA", f"{overview['avg_gpa']:.2f}")
    col3.metric("Average Attendance", f"{overview['avg_attendance']:.1f}%")
    col4.metric("Average Study Hours", f"{overview['avg_study_hours']:.1f} hrs")

    col5, col6 = st.columns(2)
    with col5:
        fig_hist = px.histogram(
            df,
            x="gpa",
            nbins=20,
            title="GPA Distribution",
            color_discrete_sequence=["#4c78a8"],
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col6:
        fig_major = px.bar(
            summarize_by_major(df),
            x="major",
            y="average_gpa",
            title="Average GPA by Major",
            color="average_gpa",
            color_continuous_scale="Viridis",
        )
        st.plotly_chart(fig_major, use_container_width=True)

    st.subheader("Academic Performance")
    c1, c2 = st.columns(2)
    with c1:
        fig_year = px.line(
            summarize_by_year(df),
            x="academic_year",
            y="average_gpa",
            title="Average GPA by Academic Year",
            markers=True,
        )
        st.plotly_chart(fig_year, use_container_width=True)

    with c2:
        fig_attend = px.scatter(
            df,
            x="attendance_percentage",
            y="gpa",
            title="Attendance vs GPA",
            color="major",
            hover_data=["student_id"],
        )
        st.plotly_chart(fig_attend, use_container_width=True)

    st.subheader("Study Habits")
    c3, c4 = st.columns(2)
    with c3:
        fig_study = px.scatter(
            df,
            x="study_hours_per_week",
            y="gpa",
            title="Study Hours vs GPA",
            color="academic_year",
            hover_data=["student_id"],
        )
        st.plotly_chart(fig_study, use_container_width=True)

    with c4:
        fig_sleep = px.scatter(
            df,
            x="sleep_hours_per_night",
            y="gpa",
            title="Sleep Hours vs GPA",
            color="attendance_percentage",
            hover_data=["student_id"],
        )
        st.plotly_chart(fig_sleep, use_container_width=True)

    st.subheader("Student Groups")
    attendance_summary = summarize_attendance_groups(df)
    fig_group = px.bar(
        attendance_summary,
        x="attendance_group",
        y="average_gpa",
        title="Average GPA by Attendance Group",
        color="attendance_group",
    )
    st.plotly_chart(fig_group, use_container_width=True)

    st.subheader("Key Relationships")
    relationships = get_top_relationships(df)
    for feature, target, value in relationships:
        st.write(f"- {feature.replace('_', ' ').title()}: correlation with GPA = {value}")

    st.info(
        "These findings are patterns in the dataset and should not be interpreted as proof that one factor directly causes another."
    )


if __name__ == "__main__":
    run_dashboard()
