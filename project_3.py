import os
from pathlib import Path
import PyPDF2

# Constants
CONTENT_FOLDER = "./content"
PDF_FILE = "Chemistry Questions.pdf"
OUTPUT_FILE = "output.txt"

def read_pdf_page_content(pdf_path, page_number):
    """Reads content from a specific page of a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if page_number < 1 or page_number > len(reader.pages):
                raise ValueError(f"Page number {page_number} is out of range. The PDF has {len(reader.pages)} pages.")
            page_content = reader.pages[page_number - 1].extract_text()
            return page_content
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file '{pdf_path}' not found.")
    except Exception as e:
        raise Exception(f"Error reading PDF file: {e}")

def write_to_text_file(content, text_path):
    """Writes content to a text file."""
    try:
        with open(text_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        raise Exception(f"Error writing to text file: {e}")

def main():
    pdf_path = Path(CONTENT_FOLDER) / PDF_FILE
    output_path = Path(CONTENT_FOLDER) / OUTPUT_FILE

    try:
        # Prompt user for page number
        page_number = int(input("Enter the page number to read content from: "))
        # Read content from the specified page
        content = read_pdf_page_content(pdf_path, page_number)
        # Write content to the output file
        write_to_text_file(content, output_path)
        print(f"Content from page {page_number} successfully written to '{output_path}'.")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
