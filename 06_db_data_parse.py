import sqlite3
import os

os.makedirs("data/db", exist_ok=True)

# Create a sample SQLite database and table
conn = sqlite3.connect("data/db/company.db")
cursor = conn.cursor()

cursor.execute(
    """
               CREATE TABLE IF NOT EXISTS employees (
                     id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     role TEXT NOT NULL,
                     department TEXT NOT NULL,
                     salary REAL NOT NULL
                )
                """
)

cursor.execute(
    """
               CREATE TABLE IF NOT EXISTS projects (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        status TEXT,
                        budget REAL,
                        lead_id INTEGER,
                    )
                    """
)

employees = [
    (1, "Alice Johnson", "Software Engineer", "Development", 90000),
    (2, "Bob Smith", "Data Scientist", "Data Science", 95000),
    (3, "Charlie Brown", "Product Manager", "Product", 105000),
    (4, "Diana Prince", "UX Designer", "Design", 85000),
]

projects = [
    (1, "Project Apollo", "Active", 500000, 3),
    (2, "Project Zeus", "Completed", 300000, 2),
    (3, "Project Hera", "Planning", 150000, 1),
]
