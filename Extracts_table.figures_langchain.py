import os
import shutil
import pdfplumber
import pandas as pd
import re
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

# Set working directory path
os.chdir("/Users/iriskim/Desktop/PCORI/Meta_VERSA")

# Define input and output folders
input_pdf_files = Path("Full text pdf_Versa Ruled in")
output_pdf_files = Path("Extracted_PDFs_xlsx_tables")

# Ensure output directory exists and is cleared
if not output_pdf_files.exists():
    os.makedirs(output_pdf_files)
    print(f"Folder {output_pdf_files} was created.")
else:
    print(f"Folder {output_pdf_files} already exists.")
    for filename in os.listdir(output_pdf_files):
        file_path = os.path.join(output_pdf_files, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    print(f"All contents removed from {output_pdf_files}.")

def extract_tables_from_pdf(pdf_path, output_folder):
    with pdfplumber.open(pdf_path) as pdf:
        table_count = 0
        for i, page in enumerate(pdf.pages):
            text = page.extract_text(x_tolerance=3, y_tolerance=3)  # Preserve formatting
            tables = page.extract_tables()
            
            if not text:
                continue
            
            lines = text.split("\n")
            
            for table in tables:
                if table and any(any(cell and str(cell).isalnum() for cell in row) for row in table):  # Ensure table is not empty
                    
                    # Identify the table name
                    table_name = None
                    column_names = []
                    first_row_first_cell = table[0][0] if table and table[0] else None
                    
                    for j in range(len(lines) - 1):
                        if "Table" in lines[j] and any(char.isdigit() for char in lines[j]):
                            table_name = lines[j].replace("\t", "    ")  # Preserve spaces/tabs
                            column_names = []
                            # Collect column names (lines after the table name, stopping when first row's first cell appears)
                            for k in range(j + 1, len(lines)):
                                if first_row_first_cell and first_row_first_cell.strip() in lines[k]:
                                    break
                                column_names.extend(lines[k].split(" "))
                            break
                    
                    cleaned_columns = [col.strip() for col in column_names if col.strip()]
                    df = pd.DataFrame(table)
                    
                    if cleaned_columns and len(cleaned_columns) == len(df.columns):
                        df.columns = cleaned_columns
                    
                    table_count += 1
                    output_file = output_folder / f"{pdf_path.stem}_Table_{table_count}.xlsx"
                    
                    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
                        worksheet = writer.book.add_worksheet("Table")
                        writer.sheets["Table"] = worksheet

                        # Row 0: Title
                        worksheet.write(0, 0, f"Paper Title: {pdf_path.stem}")

                        # Row 1: Table name (if found)
                        if table_name:
                            worksheet.write(1, 0, table_name)

                        # Row 2: Column headers
                        for col_idx, col_name in enumerate(cleaned_columns):
                            worksheet.write(2, col_idx, col_name)

                        # Data starts from row 3
                        for row_idx, row in enumerate(df.itertuples(index=False), start=3):
                            for col_idx, value in enumerate(row):
                                worksheet.write(row_idx, col_idx, value)

                        writer.close()

                    print(f"Saved table: {output_file}")

# Process only the test file
# test_file = "A-Carvedilol reduces the risk of decompensation and mortality in patients with compensated cirrhosis in a competing-risk meta-analysis. Càndid"


# Process only the test file
for file in input_pdf_files.rglob("*.pdf"):
    print(f"Processing: {file.name}")
    extract_tables_from_pdf(file, output_pdf_files)

print("Processing complete.")







# csv code
# import os
# import shutil
# import pdfplumber
# import pandas as pd
# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader

# # Set working directory path
# os.chdir("/Users/iriskim/Desktop/PCORI/Meta_VERSA")

# # Define input and output folders
# input_pdf_files = Path("Full text pdf_Versa Ruled in")
# output_pdf_files = Path("Extracted_PDFs_csv_tables")

# # Ensure output directory exists and is cleared
# if not output_pdf_files.exists():
#     os.makedirs(output_pdf_files)
#     print(f"Folder {output_pdf_files} was created.")
# else:
#     print(f"Folder {output_pdf_files} already exists.")
#     for filename in os.listdir(output_pdf_files):
#         file_path = os.path.join(output_pdf_files, filename)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     print(f"All contents removed from {output_pdf_files}.")

# def extract_tables_from_pdf(pdf_path, output_folder):
#     with pdfplumber.open(pdf_path) as pdf:
#         table_count = 0
#         for i, page in enumerate(pdf.pages):
#             text = page.extract_text(x_tolerance=3, y_tolerance=3)
#             tables = page.extract_tables()

#             if not text:
#                 continue

#             lines = text.split("\n")

#             for table in tables:
#                 if table and any(any(cell and str(cell).isalnum() for cell in row) for row in table):
                    
#                     table_name = None
#                     column_names = []
#                     first_row_first_cell = table[0][0] if table and table[0] else None

#                     for j in range(len(lines) - 1):
#                         if "Table" in lines[j] and any(char.isdigit() for char in lines[j]):
#                             table_name = lines[j].replace("\t", "    ")
#                             column_names = []
#                             for k in range(j + 1, len(lines)):
#                                 if first_row_first_cell and first_row_first_cell.strip() in lines[k]:
#                                     break
#                                 column_names.extend(lines[k].split(","))
#                             break

#                     cleaned_columns = [col.strip() for col in column_names if col.strip()]
#                     df = pd.DataFrame(table)

#                     if cleaned_columns and len(cleaned_columns) == len(df.columns):
#                         df.columns = cleaned_columns

#                     table_count += 1
#                     output_file = output_folder / f"{pdf_path.stem}_Table_{table_count}.csv"

#                     # Write title, table name, and then the dataframe to CSV
#                     with open(output_file, "w", encoding="utf-8", newline="") as f:
#                         f.write(f"Paper Title: {pdf_path.stem}\n")
#                         if table_name:
#                             f.write(f"{table_name}\n")
#                         df.to_csv(f, index=False)

#                     print(f"Saved table: {output_file}")

# # Process all PDF files in the input folder
# for file in input_pdf_files.rglob("*.pdf"):
#     print(f"Processing: {file.name}")
#     extract_tables_from_pdf(file, output_pdf_files)

# print("Processing complete.")












# xlsx code
# import os
# import shutil
# import pdfplumber
# import pandas as pd
# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader

# # Set working directory path
# os.chdir("/Users/iriskim/Desktop/PCORI/Meta_VERSA")

# # Define input and output folders
# input_pdf_files = Path("Full text pdf_Versa Ruled in")
# output_pdf_files = Path("Extracted_PDFs_xlsx_tables")

# # Ensure output directory exists and is cleared
# if not output_pdf_files.exists():
#     os.makedirs(output_pdf_files)
#     print(f"Folder {output_pdf_files} was created.")
# else:
#     print(f"Folder {output_pdf_files} already exists.")
#     for filename in os.listdir(output_pdf_files):
#         file_path = os.path.join(output_pdf_files, filename)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     print(f"All contents removed from {output_pdf_files}.")

# def extract_tables_from_pdf(pdf_path, output_folder):
#     with pdfplumber.open(pdf_path) as pdf:
#         table_count = 0
#         for i, page in enumerate(pdf.pages):
#             text = page.extract_text(x_tolerance=3, y_tolerance=3)  # Preserve formatting
#             tables = page.extract_tables()
            
#             if not text:
#                 continue
            
#             lines = text.split("\n")
            
#             for table in tables:
#                 if table and any(any(cell and str(cell).isalnum() for cell in row) for row in table):  # Ensure table is not empty
                    
#                     # Identify the table name
#                     table_name = None
#                     column_names = []
#                     first_row_first_cell = table[0][0] if table and table[0] else None
                    
#                     for j in range(len(lines) - 1):
#                         if "Table" in lines[j] and any(char.isdigit() for char in lines[j]):
#                             table_name = lines[j].replace("\t", "    ")  # Preserve spaces/tabs
#                             column_names = []
#                             # Collect column names (lines after the table name, stopping when first row's first cell appears)
#                             for k in range(j + 1, len(lines)):
#                                 if first_row_first_cell and first_row_first_cell.strip() in lines[k]:
#                                     break
#                                 column_names.extend(lines[k].split(","))
#                             break
                    
#                     cleaned_columns = [col.strip() for col in column_names if col.strip()]
#                     df = pd.DataFrame(table)
                    
#                     if cleaned_columns and len(cleaned_columns) == len(df.columns):
#                         df.columns = cleaned_columns
                    
#                     table_count += 1
#                     output_file = output_folder / f"{pdf_path.stem}_Table_{table_count}.xlsx"
                    
#                     with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
#                         worksheet = writer.book.add_worksheet("Table")
#                         writer.sheets["Table"] = worksheet

#                         # Row 0: Title
#                         worksheet.write(0, 0, f"Paper Title: {pdf_path.stem}")

#                         # Row 1: Table name (if found)
#                         if table_name:
#                             worksheet.write(1, 0, table_name)

#                         # Row 2: Column headers
#                         for col_idx, col_name in enumerate(cleaned_columns):
#                             worksheet.write(2, col_idx, col_name)

#                         # Data starts from row 3
#                         for row_idx, row in enumerate(df.itertuples(index=False), start=3):
#                             for col_idx, value in enumerate(row):
#                                 worksheet.write(row_idx, col_idx, value)

#                         writer.close()

#                     print(f"Saved table: {output_file}")

# # Process only the test file
# # test_file = "A-Carvedilol reduces the risk of decompensation and mortality in patients with compensated cirrhosis in a competing-risk meta-analysis. Càndid"


# # Process only the test file
# for file in input_pdf_files.rglob("*.pdf"):
#     print(f"Processing: {file.name}")
#     extract_tables_from_pdf(file, output_pdf_files)

# print("Processing complete.")




# import os
# import shutil
# import pdfplumber
# import pandas as pd
# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader

# # Set working directory path
# os.chdir("/Users/iriskim/Desktop/PCORI/Meta_VERSA")

# # Define input and output folders
# input_pdf_files = Path("Full text pdf_Versa Ruled in")
# output_pdf_files = Path("Extracted_PDFs_test3")

# # Ensure output directory exists and is cleared
# if not output_pdf_files.exists():
#     os.makedirs(output_pdf_files)
#     print(f"Folder {output_pdf_files} was created.")
# else:
#     print(f"Folder {output_pdf_files} already exists.")
#     for filename in os.listdir(output_pdf_files):
#         file_path = os.path.join(output_pdf_files, filename)
#         if os.path.isfile(file_path):
#             os.remove(file_path)
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
#     print(f"All contents removed from {output_pdf_files}.")

# # Function to extract tables from PDF with table names (preserving spaces)
# def extract_tables_from_pdf(pdf_path, output_folder):
#     with pdfplumber.open(pdf_path) as pdf:
#         table_count = 0
#         for i, page in enumerate(pdf.pages):
#             text = page.extract_text(x_tolerance=3, y_tolerance=3)  # Preserve formatting
#             tables = page.extract_tables()

#             for table in tables:
#                 if table and any(any(cell and str(cell).isalnum() for cell in row) for row in table):  # Ensure table is not empty
                    
#                     # Try to find table name above the table in text
#                     lines = text.split("\n") if text else []
#                     table_name = None
#                     for j in range(len(lines) - 1):
#                         if "Table" in lines[j] and any(char.isdigit() for char in lines[j]):  # Identify table titles
#                             table_name = lines[j].replace("\t", "    ")  # Preserve spaces/tabs
#                             break
                    
#                     # Convert table to DataFrame
#                     df = pd.DataFrame(table)

#                     table_count += 1
#                     output_file = output_folder / f"{pdf_path.stem}_Table_{table_count}.xlsx"

#                     # Save to Excel with table name in first row, data in second row
#                     with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
#                         worksheet = writer.book.add_worksheet("Table")
#                         writer.sheets["Table"] = worksheet

#                         # Write table name in first row (A1) without altering spaces
#                         if table_name:
#                             worksheet.write(0, 0, table_name)  

#                         # Write table data starting from second row
#                         for row_idx, row in enumerate(df.itertuples(index=False), start=1):
#                             for col_idx, value in enumerate(row):
#                                 worksheet.write(row_idx, col_idx, value)

#                         writer.close()
                        
#                     print(f"Saved table: {output_file}")

# # Process only the test file
# # test_file = "A-Carvedilol reduces the risk of decompensation and mortality in patients with compensated cirrhosis in a competing-risk meta-analysis. Càndid"

# for file in input_pdf_files.rglob("*.pdf"):
#     print(f"Processing: {file.name}")
#     extract_tables_from_pdf(file, output_pdf_files)

# print("Processing complete.")