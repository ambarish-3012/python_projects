import os
from pathlib import Path
import PyPDF2

# Constants
CONTENT_FOLDER = "./"
PDF_FILE = "Chemistry Questions.pdf"
OUTPUT_FILE = "output.txt"

def read_pdf_content(pdf_path):
    """Reads content from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
            return content
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
        # Read the PDF content
        content = read_pdf_content(pdf_path)

        # Write to the output.txt file
        write_to_text_file(content, output_path)

        print(f"PDF content successfully written to '{output_path}'.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
