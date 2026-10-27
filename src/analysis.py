from __future__ import annotations

from typing import Dict, List

import pandas as pd


def get_overview_stats(df: pd.DataFrame) -> Dict[str, float]:
    """Return summary metrics for the dashboard overview."""
    return {
        "total_students": int(df.shape[0]),
        "avg_gpa": round(float(df["gpa"].mean()), 2),
        "avg_attendance": round(float(df["attendance_percentage"].mean()), 1),
        "avg_study_hours": round(float(df["study_hours_per_week"].mean()), 2),
        "avg_academic_score": round(float(df["academic_score"].mean()), 1),
    }


def summarize_by_major(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("major", as_index=False)
        .agg(
            average_gpa=("gpa", "mean"),
            average_attendance=("attendance_percentage", "mean"),
            average_study_hours=("study_hours_per_week", "mean"),
            student_count=("student_id", "count"),
        )
        .sort_values("average_gpa", ascending=False)
        .reset_index(drop=True)
    )


def summarize_by_year(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("academic_year", as_index=False)
        .agg(
            average_gpa=("gpa", "mean"),
            average_attendance=("attendance_percentage", "mean"),
            average_study_hours=("study_hours_per_week", "mean"),
            student_count=("student_id", "count"),
        )
        .sort_values("academic_year")
        .reset_index(drop=True)
    )


def summarize_attendance_groups(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["attendance_group"] = pd.cut(
        df["attendance_percentage"],
        bins=[0, 79, 89, 100],
        labels=["Low Attendance", "Medium Attendance", "High Attendance"],
        include_lowest=True,
    )
    return (
        df.groupby("attendance_group", observed=False)
        .agg(
            average_gpa=("gpa", "mean"),
            average_attendance=("attendance_percentage", "mean"),
            average_study_hours=("study_hours_per_week", "mean"),
            student_count=("student_id", "count"),
        )
        .reset_index()
        .sort_values("average_gpa", ascending=False)
    )


def get_top_relationships(df: pd.DataFrame) -> List[tuple[str, str, float]]:
    correlations = []
    for column in [
        "study_hours_per_week",
        "attendance_percentage",
        "assignment_completion_rate",
        "sleep_hours_per_night",
        "extracurricular_hours_per_week",
    ]:
        corr_value = df[column].corr(df["gpa"])
        correlations.append((column, "gpa", round(float(corr_value), 3)))
    return sorted(correlations, key=lambda x: abs(x[2]), reverse=True)
