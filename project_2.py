import os
from pathlib import Path
import PyPDF2

# Constants
BASE_FOLDER = "./content"
OUTPUT_FILE_NAME = "output.txt"

def read_pdf_content(pdf_path):
    """Reads content from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
            return content
    except Exception as e:
        return f"Error reading {pdf_path}: {e}"

def write_to_text_file(content, text_path):
    """Writes content to a text file."""
    try:
        with open(text_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        raise Exception(f"Error writing to text file: {e}")

def process_folder(folder_path):
    """Processes all PDF files in a folder."""
    output_file_path = Path(folder_path) / OUTPUT_FILE_NAME
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in '{folder_path}'.")
        return

    combined_content = ""
    for pdf_file in pdf_files:
        pdf_path = Path(folder_path) / pdf_file
        content = read_pdf_content(pdf_path)
        combined_content += f"\n--- Content from {pdf_file} ---\n" + content

    write_to_text_file(combined_content, output_file_path)
    print(f"Content written to '{output_file_path}'.")

def main():
    # Process each subfolder
    base_path = Path(BASE_FOLDER)
    for subfolder in base_path.iterdir():
        if subfolder.is_dir():
            process_folder(subfolder)

if __name__ == "__main__":
    main()
