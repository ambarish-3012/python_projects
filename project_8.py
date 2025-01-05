import mysql.connector
from abc import ABC, abstractmethod

# Database Configuration
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root@dec30',  # Replace with your MySQL root password
    'database': 'question_bank'
}

# Base Class for Questions
class Question(ABC):
    def __init__(self, subject, chapter, question_text):
        self.subject = subject
        self.chapter = chapter
        self.question_text = question_text

    @abstractmethod
    def save_to_database(self, connection):
        pass

# Subjective Question
class SubjectiveQuestion(Question):
    def __init__(self, subject, chapter, question_text, answer):
        super().__init__(subject, chapter, question_text)
        self.answer = answer

    def save_to_database(self, connection):
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO questions (subject_name, chapter_name, question_type, question_text, answer_options)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.subject, self.chapter, "Subjective", self.question_text, self.answer))
        connection.commit()

# Objective Question
class ObjectiveQuestion(Question):
    def __init__(self, subject, chapter, question_text, options):
        super().__init__(subject, chapter, question_text)
        self.options = options

    def save_to_database(self, connection):
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO questions (subject_name, chapter_name, question_type, question_text, answer_options)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.subject, self.chapter, "Objective", self.question_text, ", ".join(self.options)))
        connection.commit()

# True/False Question
class TrueFalseQuestion(Question):
    def __init__(self, subject, chapter, question_text, is_true):
        super().__init__(subject, chapter, question_text)
        self.is_true = is_true

    def save_to_database(self, connection):
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO questions (subject_name, chapter_name, question_type, question_text, answer_options)
            VALUES (%s, %s, %s, %s, %s)
        """, (self.subject, self.chapter, "True/False", self.question_text, "True" if self.is_true else "False"))
        connection.commit()

def connect_to_database(config):
    """Connects to the MySQL database."""
    try:
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        raise Exception(f"Database connection error: {err}")

def main():
    try:
        # Connect to the database
        connection = connect_to_database(DATABASE_CONFIG)

        # Example questions
        q1 = SubjectiveQuestion("Chemistry", "Chapter 1", "Describe the process of photosynthesis.", "It involves the conversion of light energy to chemical energy.")
        q2 = ObjectiveQuestion("Biology", "Chapter 2", "Which of the following is a mammal?", ["Dog", "Crocodile", "Shark", "Frog"])
        q3 = TrueFalseQuestion("Physics", "Chapter 3", "The speed of light is constant.", True)

        # Save questions to the database
        q1.save_to_database(connection)
        q2.save_to_database(connection)
        q3.save_to_database(connection)

        print("Questions successfully saved to the database.")

    except Exception as e:
        print(e)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
