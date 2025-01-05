import os
from pathlib import Path
import PyPDF2
import mysql.connector
import re

# Constants
CONTENT_FOLDER = "./content"
PDF_FILE = "Chemistry Questions.pdf"
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@dec30',  # Replace with your MySQL root password
    'database': 'question_bank'
}

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

def normalize_content(content):
    """Normalizes the content to handle line breaks and spacing issues."""
    return content.replace("\r", "").replace("\n\n", "\n").strip()

def extract_questions_and_options(content):
    """
    Extracts questions and their options using robust logic.
    Handles edge cases such as missing or misaligned options.
    """
    try:
        # Normalize content
        content = normalize_content(content)

        # Split content into lines for easier processing
        lines = content.split("\n")
        extracted_data = []

        # Regex for identifying questions and options
        question_pattern = re.compile(r"^\d+\.\s*(.+)")  # Matches questions like '1. Question text'
        option_pattern = re.compile(r"^[A-D]\)\s*(.+)")  # Matches options like 'A) Option text'

        question = None
        options = []

        # Process line by line
        for line in lines:
            question_match = question_pattern.match(line)
            option_match = option_pattern.match(line)

            if question_match:
                # If a new question is found, save the previous one
                if question:
                    # Save the previous question and its options
                    extracted_data.append((question, ", ".join(options) if options else "A) Missing, B) Missing, C) Missing, D) Missing"))
                # Start a new question
                question = question_match.group(1).strip()
                options = []  # Reset options for the new question
            elif option_match:
                # Add the option to the current options list
                options.append(option_match.group(1).strip())

        # Save the last question and its options
        if question:
            extracted_data.append((question, ", ".join(options) if options else "A) Missing, B) Missing, C) Missing, D) Missing"))

        return extracted_data
    except Exception as e:
        raise Exception(f"Error extracting questions and options: {e}")

def connect_to_database(config):
    """Connects to the MySQL database."""
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        raise Exception(f"Database connection error: {err}")

def create_table_if_not_exists(connection):
    """Creates the questions table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                subject_name VARCHAR(255),
                chapter_name VARCHAR(255),
                question_text TEXT,
                answer_options TEXT
            )
        """)
        connection.commit()
    except mysql.connector.Error as err:
        raise Exception(f"Error creating table: {err}")

def insert_question_into_db(connection, subject, chapter, question, options):
    """Inserts a question into the database."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO questions (subject_name, chapter_name, question_text, answer_options)
            VALUES (%s, %s, %s, %s)
        """, (subject, chapter, question, options))
        connection.commit()
    except mysql.connector.Error as err:
        raise Exception(f"Error inserting question: {err}")

def main():
    pdf_path = Path(CONTENT_FOLDER) / PDF_FILE

    try:
        # Read content from the PDF
        content = read_pdf_content(pdf_path)

        # Extract questions and their options
        extracted_data = extract_questions_and_options(content)

        # Connect to the database
        connection = connect_to_database(DATABASE_CONFIG)

        # Ensure the table exists
        create_table_if_not_exists(connection)

        # Insert each question and its options into the database
        for idx, (question, options) in enumerate(extracted_data, start=1):
            subject = "Chemistry"
            chapter = f"Chapter {idx}"
            insert_question_into_db(connection, subject, chapter, question, options)

        print(f"{len(extracted_data)} questions successfully stored in the database.")
    except Exception as e:
        print(e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
