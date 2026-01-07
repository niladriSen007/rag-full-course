import pandas as pd
import os
from langchain_community.document_loaders import CSVLoader
from typing import List
from langchain_core.documents import Document

os.makedirs("data/csv_excel", exist_ok=True)

# Create a sample CSV file
data = {
    "Products": ["Laptop", "Smartphone", "Tablet", "Monitor"],
    "Prices": [1200, 800, 300, 400],
    "Stock": [50, 200, 150, 80],
    "Category": ["Electronics", "Accessories", "Electronics", "Accessories"],
    "Description": [
        "High-performance laptop",
        "Latest model smartphone",
        "Lightweight tablet",
        "4K UHD monitor",
    ],
}
## save csv file
df = pd.DataFrame(data)

csv_path = "data/csv_excel/products.csv"
df.to_csv(csv_path, index=False)
print(f"Sample CSV file created at: {csv_path}")


## save as excel
with pd.ExcelWriter("data/csv_excel/products.xlsx") as writer:
    df.to_excel(writer, index=False, sheet_name="Products")
    # summary_data = {
    #     "Category": ["Electronics", "Accessories"],
    #     "Total Products": [len(data["Products"])],
    #     "Average Price": [sum(data["Prices"]) / len(data["Prices"])],
    #     "Total Stock": [sum(data["Stock"])],
    #     "Description Sample": ["High-performance laptop, Latest model smartphone"],
    # }
    # summary_df = pd.DataFrame(summary_data)
    # summary_df.to_excel(writer, index=False, sheet_name="Summary")
print("Sample Excel file created at: data/csv_excel/products.xlsx")

## loading the CSV file using CSVLoader
try:
    ## storing each row as a document
    csv_loader = CSVLoader(
        file_path=csv_path,
        encoding="utf-8",
        csv_args={
            "delimiter": ",",
            "quotechar": '"',
        },
    )
    documents = csv_loader.load()
    # print(f"Loaded {len(documents)} documents from CSV file.")
    # print(documents[0].page_content)  # Print content of the first document
    # print(f"Metadata: {documents[0].metadata}")
except Exception as e:
    print(f"CSVLoader failed with error: {e}")


def smart_csv_loader(file_path: str) -> List[Document]:
    """Process CSV with intelligent document creation"""
    data = pd.read_csv(file_path)
    docs = []
    ## one document per row with enhanced structured content
    for idx, row in data.iterrows():
        content = f"""
            Product information:
            - Name: {row['Products']}
            - Price: ${row['Prices']}
            - Stock: {row['Stock']} units
            - Category: {row['Category']}
            - Description: {row['Description']}
        """
        ## create a document with metadata
        doc = Document(
            page_content=content,
            metadata={
                "row_index": idx,
                "product_name": row["Products"],
                "price": row["Prices"],
                "stock": row["Stock"],
                "category": row["Category"],
            },
        )
        docs.append(doc)
    return docs


result = smart_csv_loader(csv_path)
# print(f"Smart CSV Loader created {len(result)} documents.")
# print(result[0])


def smart_excel_loader(file_path: str) -> List[Document]:
    """Process Excel with intelligent document creation"""
    docs = []
    excel_files = pd.ExcelFile(file_path)
    for sheet_name in excel_files.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # create document for each sheet
        sheet_content = f"Sheet: {sheet_name}\n"
        sheet_content += f"Columns : {', '.join(df.columns)}\n\n"
        sheet_content += f"Rows: {len(df)}\n\n"
        sheet_content += f"Content: {df.to_string(index=False)}\n"
        doc = Document(
            page_content=sheet_content,
            metadata={
                "source": file_path,
                "sheet_name": sheet_name,
                "num_rows": len(df),
                "num_columns": len(df.columns),
                "data_type": "excel_sheet",
            },
        )
        docs.append(doc)
    return docs

excel_path = "data/csv_excel/products.xlsx"
excel_docs = smart_excel_loader(excel_path)
print(f"Smart Excel Loader created {len(excel_docs)} documents.")
print(excel_docs[0])