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
                        lead_id INTEGER
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

cursor.executemany(
    "INSERT OR REPLACE INTO employees (id, name, role, department, salary) VALUES (?, ?, ?, ?, ?)",
    employees,
)

cursor.executemany(
    "INSERT OR REPLACE INTO projects (id, name, status, budget, lead_id) VALUES (?, ?, ?, ?, ?)",
    projects,
)

conn.commit()
conn.close()


from langchain_community.utilities import SQLDatabase
from langchain_community.document_loaders import SQLDatabaseLoader
from typing import List
from langchain_core.documents import Document

# Loading the SQLite database using SQLiteLoader
db = SQLDatabase.from_uri("sqlite:///data/db/company.db")
def smart_db_loader(path:str) -> List[Document]:
    """Convert a SQL database to a list of Documents with rich context."""
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        docs = []
        # Strategy 1: Create documents for each table with schema info
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            # get table data
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            
            # create a table overview document
            table_content = f"Table name: {table_name}\n"
            table_content += f"Columns: {', '.join(column_names)}\n\n"
            table_content+= f"Total records: {len(rows)}\n\n"
            
            # add sample records
            table_content += "Sample Records:\n"
            for row in rows[:5]:  # limit to first 5 records
                record = dict(zip(column_names, row))
                table_content += f"{record}\n"
      
            doc = Document(
                page_content=table_content,
                metadata={
                    "source": path,
                    "table_name": table_name,
                    "num_columns": len(column_names),
                    "num_records": len(rows),
                    "data_type": "sql_table",
                },
            )
            docs.append(doc)
        connection.close()
        return docs
    except Exception as e:
        print(f"SQLiteLoader failed with error: {e}")


result = smart_db_loader("data/db/company.db")
print(f"Smart DB Loader created {len(result)} documents.")
print(result[0])