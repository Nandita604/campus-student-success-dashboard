-- Average GPA by major
SELECT
    major,
    ROUND(AVG(gpa), 2) AS average_gpa,
    ROUND(AVG(attendance_percentage), 2) AS average_attendance,
    ROUND(AVG(study_hours_per_week), 2) AS average_study_hours
FROM students
GROUP BY major
ORDER BY average_gpa DESC;

-- Academic performance by year
SELECT
    academic_year,
    ROUND(AVG(gpa), 2) AS average_gpa,
    ROUND(AVG(attendance_percentage), 2) AS average_attendance,
    ROUND(AVG(study_hours_per_week), 2) AS average_study_hours
FROM students
GROUP BY academic_year
ORDER BY academic_year;

-- Attendance groups
SELECT
    CASE
        WHEN attendance_percentage >= 90 THEN 'High Attendance'
        WHEN attendance_percentage >= 80 THEN 'Medium Attendance'
        ELSE 'Low Attendance'
    END AS attendance_group,
    ROUND(AVG(gpa), 2) AS average_gpa,
    COUNT(*) AS student_count
FROM students
GROUP BY attendance_group
ORDER BY average_gpa DESC;
