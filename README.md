# Campus Student Success Dashboard

A data analytics dashboard that explores the relationship between academic performance and student factors such as study habits, attendance, extracurricular activities, and other demographic or behavioral attributes.

This project uses Python, SQL, Pandas, and Streamlit to transform raw student data into interactive visualizations and data-driven insights.

## Problem Statement

Universities collect large amounts of student information, but raw data alone does not provide an easy way to identify meaningful patterns.

This project answers questions such as:
- What factors are associated with higher academic performance?
- How does study time relate to GPA or academic scores?
- Is attendance associated with academic performance?
- Do extracurricular activities show any relationship with academic outcomes?
- How do these patterns vary across different student groups?
- Can interactive data visualization make these insights easier to understand?

The goal is not to predict or label individual students, but to explore aggregated patterns in the dataset and demonstrate how data can support informed decision-making.

## Project Objectives

1. Collect or use a suitable publicly available student dataset.
2. Clean and prepare the data using Python and Pandas.
3. Store and query structured data using SQL.
4. Perform exploratory data analysis.
5. Identify relationships and trends between student attributes and academic outcomes.
6. Build an interactive dashboard using Streamlit.
7. Present findings through clear visualizations.
8. Document the methodology, limitations, and potential improvements.

## Features

- Student performance overview with KPI cards
- GPA distribution and major comparison
- Academic year trends and attendance analysis
- Study habits correlation analysis
- Filterable dashboard by academic year, major, and gender
- SQL-backed data exploration example
- Synthetic sample dataset for portfolio use

## Technology Stack

- Python
- Pandas / NumPy
- SQLite / SQL
- Matplotlib / Plotly
- Streamlit

## Project Structure

```text
campus-student-success-dashboard/
├── data/
│   ├── raw/
│   │   └── students.csv
│   └── processed/
│       └── cleaned_students.csv
├── notebooks/
│   └── exploratory_analysis.ipynb
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── database.py
├── dashboard/
│   └── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

## Dataset

This project includes a synthetic dataset for demonstration purposes.

- Dataset: Synthetic student performance dataset
- Source: Generated for educational and portfolio use
- Location: `data/raw/students.csv`

## Data Preparation

Before analysis, the dataset is processed to:
- remove duplicate records
- handle missing values
- normalize column names
- validate numeric ranges
- convert categorical values where necessary

## SQL Analysis

Sample SQL query:

```sql
SELECT
    major,
    ROUND(AVG(gpa), 2) AS average_gpa,
    ROUND(AVG(attendance_percentage), 2) AS average_attendance,
    ROUND(AVG(study_hours_per_week), 2) AS average_study_hours
FROM students
GROUP BY major
ORDER BY average_gpa DESC;
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Nandita604/campus-student-success-dashboard.git
cd campus-student-success-dashboard
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard

```bash
streamlit run dashboard/app.py
```

## Example Insights

This dataset is synthetic, but it supports examples like:
- students with higher attendance tend to have higher GPAs
- study hours and assignment completion are associated with stronger academic performance overall
- some majors show higher average GPA, though differences should be interpreted as observed patterns in the data rather than proof of causation

## What I Learned

- Python data cleaning and analysis
- SQL querying and aggregation
- Data visualization for academic insights
- Dashboard design with Streamlit
- Distinguishing correlation from causation in observational data

## Limitations

- This dataset is synthetic and not representative of a real university population
- Observed patterns do not imply causation
- The project is intended for educational and portfolio use

## Future Improvements

- add live database support
- include machine learning predictions
- add interactive SQL query interface
- deploy to Streamlit Community Cloud

## Author

Nandita Lajeesh

## License

This project is intended for educational and portfolio purposes.
