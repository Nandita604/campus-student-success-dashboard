from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "students.csv"
PROCESSED_DATA_PATH = BASE_DIR / "data" / "processed" / "cleaned_students.csv"


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load raw student dataset and perform basic validation."""
    df = pd.read_csv(path)
    expected_columns = [
        "student_id",
        "academic_year",
        "major",
        "gender",
        "study_hours_per_week",
        "attendance_percentage",
        "assignment_completion_rate",
        "sleep_hours_per_night",
        "extracurricular_hours_per_week",
        "gpa",
        "academic_score",
    ]
    missing = [col for col in expected_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")
    return df


def clean_student_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the student dataset."""
    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    numeric_cols = [
        "academic_year",
        "study_hours_per_week",
        "attendance_percentage",
        "assignment_completion_rate",
        "sleep_hours_per_night",
        "extracurricular_hours_per_week",
        "gpa",
        "academic_score",
    ]

    for col in numeric_cols:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="coerce")

    cleaned["major"] = cleaned["major"].astype(str).str.strip()
    cleaned["gender"] = cleaned["gender"].astype(str).str.strip()

    cleaned["academic_year"] = cleaned["academic_year"].fillna(cleaned["academic_year"].median())
    cleaned["study_hours_per_week"] = cleaned["study_hours_per_week"].fillna(cleaned["study_hours_per_week"].median())
    cleaned["attendance_percentage"] = cleaned["attendance_percentage"].fillna(cleaned["attendance_percentage"].median())
    cleaned["assignment_completion_rate"] = cleaned["assignment_completion_rate"].fillna(cleaned["assignment_completion_rate"].median())
    cleaned["sleep_hours_per_night"] = cleaned["sleep_hours_per_night"].fillna(cleaned["sleep_hours_per_night"].median())
    cleaned["extracurricular_hours_per_week"] = cleaned["extracurricular_hours_per_week"].fillna(cleaned["extracurricular_hours_per_week"].median())
    cleaned["gpa"] = cleaned["gpa"].fillna(cleaned["gpa"].median())
    cleaned["academic_score"] = cleaned["academic_score"].fillna(cleaned["academic_score"].median())

    cleaned["attendance_percentage"] = cleaned["attendance_percentage"].clip(0, 100)
    cleaned["assignment_completion_rate"] = cleaned["assignment_completion_rate"].clip(0, 100)
    cleaned["study_hours_per_week"] = cleaned["study_hours_per_week"].clip(lower=0)
    cleaned["sleep_hours_per_night"] = cleaned["sleep_hours_per_night"].clip(lower=0)
    cleaned["extracurricular_hours_per_week"] = cleaned["extracurricular_hours_per_week"].clip(lower=0)
    cleaned["gpa"] = cleaned["gpa"].clip(0, 4)
    cleaned["academic_score"] = cleaned["academic_score"].clip(0, 100)

    return cleaned


def save_processed_data(df: pd.DataFrame, path: Path = PROCESSED_DATA_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def prepare_data() -> pd.DataFrame:
    raw_df = load_raw_data()
    cleaned_df = clean_student_data(raw_df)
    save_processed_data(cleaned_df)
    return cleaned_df


if __name__ == "__main__":
    prepare_data()
    print(f"Processed data saved to: {PROCESSED_DATA_PATH}")
