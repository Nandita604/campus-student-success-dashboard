from __future__ import annotations

from pathlib import Path
import sqlite3

import pandas as pd

from src.data_cleaning import prepare_data

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "student_success.db"
SQL_SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    df = prepare_data()
    with sqlite3.connect(DB_PATH) as conn:
        with open(SQL_SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        df.to_sql("students", conn, if_exists="replace", index=False)


def load_students_df() -> pd.DataFrame:
    if not DB_PATH.exists():
        initialize_database()
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query("SELECT * FROM students", conn)


def get_major_summary() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            """
            SELECT major,
                   ROUND(AVG(gpa), 2) AS average_gpa,
                   ROUND(AVG(attendance_percentage), 2) AS average_attendance,
                   ROUND(AVG(study_hours_per_week), 2) AS average_study_hours,
                   COUNT(*) AS student_count
            FROM students
            GROUP BY major
            ORDER BY average_gpa DESC;
            """,
            conn,
        )


def get_overview_metrics() -> dict:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            """
            SELECT
                COUNT(*) AS total_students,
                AVG(gpa) AS avg_gpa,
                AVG(attendance_percentage) AS avg_attendance,
                AVG(study_hours_per_week) AS avg_study_hours,
                AVG(academic_score) AS avg_academic_score
            FROM students;
            """
        ).fetchone()
    return {
        "total_students": row[0],
        "avg_gpa": round(row[1], 2) if row[1] else 0,
        "avg_attendance": round(row[2], 2) if row[2] else 0,
        "avg_study_hours": round(row[3], 2) if row[3] else 0,
        "avg_academic_score": round(row[4], 2) if row[4] else 0,
    }


if __name__ == "__main__":
    initialize_database()
    print(f"Database created at: {DB_PATH}")
