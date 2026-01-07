import json
import os
from langchain_community.document_loaders import JSONLoader
from typing import List

os.makedirs("data/json", exist_ok=True)

# Create a sample JSON file
json_data = {
    "company": "Codusa",
    "employees": [
        {
            "id": 1,
            "name": "Alice Johnson",
            "department": "Engineering",
            "role": "Software Engineer",
            "salary": 95000,
        },
        {
            "id": 2,
            "name": "Bob Smith",
            "department": "Marketing",
            "role": "Marketing Manager",
            "salary": 85000,
        },
        {
            "id": 3,
            "name": "Charlie Brown",
            "department": "Sales",
            "role": "Sales Executive",
            "salary": 75000,
        },
    ],
}

json_path = "data/json/sample_data.json"
with open(json_path, "w") as f:
    json.dump(json_data, f, indent=4)
print(f"Sample JSON file created at: {json_path}")
# Loading the JSON file using JSONLoader
try:
    json_loader = JSONLoader(
        file_path=json_path,
        jq_schema=".employees[]",  # Each object in the array will be a separate document
        text_content=False,  # Use structured data instead of raw text
    )
    documents = json_loader.load()
    print(f"Loaded {len(documents)} documents from JSON file.")
    # print(documents[0].page_content)  # Print content of the first document
    # print(f"Metadata: {documents[0].metadata}")
except Exception as e:
    print(f"JSONLoader failed with error: {e}")
