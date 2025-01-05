import mysql.connector

# Constants
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@dec30',  # Replace with your MySQL root password
    'database': 'question_bank'
}

def connect_to_database(config):
    """Connects to the MySQL database."""
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        raise Exception(f"Database connection error: {err}")

def fetch_questions_by_chapter(connection, chapter_name):
    """Fetches all questions from a specific chapter."""
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT question_text, answer_options 
            FROM questions
            WHERE chapter_name = %s
        """, (chapter_name,))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        raise Exception(f"Error fetching questions: {err}")

def main():
    try:
        # Prompt user for chapter name
        user_input = input("Enter the chapter number to fetch questions from: ").strip()
        if not user_input:
            raise ValueError("Chapter number cannot be an empty string.")
        
        # Format the chapter name
        chapter_name = f"Chapter {user_input}"

        # Connect to the database
        connection = connect_to_database(DATABASE_CONFIG)

        # Fetch questions from the specified chapter
        questions = fetch_questions_by_chapter(connection, chapter_name)

        if not questions:
            print(f"No questions found for chapter '{chapter_name}'.")
            return

        # Print questions to the console
        print(f"Questions from chapter '{chapter_name}':\n")
        for idx, question in enumerate(questions, start=1):
            print(f"{idx}. {question['question_text']}")
            print(f"   Options: {question['answer_options']}\n")

    except ValueError as ve:
        print(f"Input error: {ve}")
    except Exception as e:
        print(e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
