DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    academic_year INTEGER,
    major TEXT,
    gender TEXT,
    study_hours_per_week REAL,
    attendance_percentage REAL,
    assignment_completion_rate REAL,
    sleep_hours_per_night REAL,
    extracurricular_hours_per_week REAL,
    gpa REAL,
    academic_score REAL
);
