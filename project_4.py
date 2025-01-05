import os
import re
import json
from pathlib import Path
import PyPDF2

# Constants
CONTENT_FOLDER = "./content"
PDF_FILE = "Chemistry Questions.pdf"
CONFIG_FILE = "config.json"
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

def read_config(config_path):
    """Reads the configuration file for the regex."""
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            if "regex" not in config or not config["regex"]:
                raise ValueError("Configuration file does not contain a valid 'regex' key.")
            return config["regex"]
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    except json.JSONDecodeError:
        raise ValueError("Configuration file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error reading configuration file: {e}")

def extract_regex_matches(content, regex):
    """Extracts content matching the regular expression."""
    try:
        matches = re.findall(regex, content)
        return "\n".join(matches) if matches else "No matches found."
    except re.error as e:
        raise ValueError(f"Invalid regular expression: {e}")

def write_to_text_file(content, text_path):
    """Writes content to a text file."""
    try:
        with open(text_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        raise Exception(f"Error writing to text file: {e}")

def main():
    pdf_path = Path(CONTENT_FOLDER) / PDF_FILE
    config_path = Path(CONTENT_FOLDER) / CONFIG_FILE
    output_path = Path(CONTENT_FOLDER) / OUTPUT_FILE

    try:
        # Read content from the PDF
        content = read_pdf_content(pdf_path)

        # Read regex from the configuration file
        regex = read_config(config_path)

        # Extract content matching the regex
        extracted_content = extract_regex_matches(content, regex)

        # Write extracted content to the output file
        write_to_text_file(extracted_content, output_path)

        print(f"Extracted content successfully written to '{output_path}'.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
