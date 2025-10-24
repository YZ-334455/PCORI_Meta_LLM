import os
import json
import shutil
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

# Set working directory path
os.chdir("/Users/iriskim/Desktop/PCORI/Meta_VERSA")

input_pdf_files = Path("Full text pdf_Versa Ruled in")
output_pdf_files = Path("Extracted_PDFs_json_txt")

# Check if output_pdf_files exists, if not create it
if not output_pdf_files.exists():
    os.makedirs(output_pdf_files)
    print(f"Folder {output_pdf_files} was created.")
else:
    print(f"Folder {output_pdf_files} already exists.")
    # Loop through the contents of the directory
    for filename in os.listdir(output_pdf_files):
        file_path = os.path.join(output_pdf_files, filename)
            
        # If it’s a file, remove it
        if os.path.isfile(file_path):
                os.remove(file_path)
        # If it’s a directory, remove the directory and its contents
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        
    print(f"All contents removed from {output_pdf_files}.")


# Function to extract text and table data from PDF
def extract_text_from_pdf(pdf_path):
    loader = PyPDFLoader(str(pdf_path))
    pages = loader.load_and_split()

    extracted_data = {"file_name": pdf_path.name, "content": []}

    for page in pages:
        # Keep all characters as they are, ensuring special characters are preserved
        page_content = page.page_content.replace("\n", "\n")  # Replace line breaks if necessary
        extracted_data["content"].append(page_content)

    return extracted_data

# Process all PDF files in the folder
for file in input_pdf_files.rglob("*.pdf"):  # Use rglob to find all .pdf files recursively
    print(f"Processing: {file.name}")
    extracted_data = extract_text_from_pdf(file)

    # Save extracted data as .txt (with real newlines)
    output_file_txt = output_pdf_files / f"{file.stem}.txt"
    with open(output_file_txt, "w", encoding="utf-8") as f:
        # Write the content to the file, using actual newlines (not \n as a string)
        for page_content in extracted_data["content"]:
            f.write(page_content + "\n")  # Writing actual newlines here

    # Save extracted data as .json (preserving structure and special characters)
    output_file_json = output_pdf_files / f"{file.stem}.json"
    with open(output_file_json, "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)

    print(f"Saved: {output_file_txt}")
    print(f"Saved: {output_file_json}")

print("Processing complete.")



# import os
# import json
# from pathlib import Path
# from langchain_community.document_loaders import PyPDFLoader



# # Set working directory path
# os.chdir("/Users/iriskim/Desktop/PCORI/Meta_VERSA")



# input_pdf_files = Path("Full text pdf_Versa Ruled in")
# output_pdf_files = Path("Extracted_PDFs")

# # Check if output_pdf_files exists, if not create it
# if not output_pdf_files.exists():
#     os.makedirs(output_pdf_files)
#     print(f"Folder {output_pdf_files} was created.")
# else:
#     print(f"Folder {output_pdf_files} already exists.")
#     # Loop through the contents of the directory
#     for filename in os.listdir(output_pdf_files):
#         file_path = os.path.join(output_pdf_files, filename)
            
#         # If it’s a file, remove it
#         if os.path.isfile(file_path):
#                 os.remove(file_path)
#         # If it’s a directory, remove the directory and its contents
#         elif os.path.isdir(file_path):
#             shutil.rmtree(file_path)
        
#     print(f"All contents removed from {output_pdf_files}.")



# # Function to extract text and table data from PDF
# def extract_text_from_pdf(pdf_path):
#     loader = PyPDFLoader(str(pdf_path))
#     pages = loader.load_and_split()

#     extracted_data = {"file_name": pdf_path.name, "content": []}

#     for page in pages:
#         # Replace '\n' with actual newlines (this will replace \n with a real line break)
#         page_content = page.page_content.replace("\n", "\n")
#         extracted_data["content"].append(page_content)

#     return extracted_data

# # Process all PDF files in the folder
# for file in input_pdf_files.rglob("*.pdf"):  # Use rglob to find all .pdf files recursively
#     print(f"Processing: {file.name}")
#     extracted_data = extract_text_from_pdf(file)

#     # Save extracted data as .txt (with real newlines)
#     output_file = output_pdf_files / f"{file.stem}.txt"
#     with open(output_file, "w", encoding="utf-8") as f:
#         # Write the content to the file, using actual newlines (not \n as a string)
#         for page_content in extracted_data["content"]:
#             f.write(page_content + "\n")  # Writing actual newlines here

#     print(f"Saved: {output_file}")

# print("Processing complete.")
