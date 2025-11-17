from tkinter import *
# In database.py
import sqlite3


class Database:
    def __init__(self, db_file):
        """
        Constructor. Stores the database file path and initializes the tables.
        """
        self.db_file = db_file
        self.initialize_database()

    def get_db_connection(self):
        """Establishes a connection to the database."""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_database(self):
        """
        Initializes the database and creates the tables if they don't already exist.
        """
        conn = self.get_db_connection()  # Use self.get_db_connection
        cursor = conn.cursor()

        # ... (all your CREATE TABLE execute statements go here, no changes)
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Students
                       (
                           student_id TEXT PRIMARY KEY,
                           first_name TEXT NOT NULL,
                           last_name TEXT NOT NULL
                       );
                       ''')
        # 2. Courses Table
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Courses
                       (
                           course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           course_name TEXT NOT NULL,
                           course_semester TEXT NOT NULL
                       );
                       ''')

        # 3. Assignments Table
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Assignments
                       (
                           assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           course_id INTEGER NOT NULL,
                           assignment_name TEXT NOT NULL,
                           assignment_type TEXT NOT NULL CHECK(assignment_type IN ('Homework', 'Test')),
                           max_points INTEGER NOT NULL,
                          FOREIGN KEY (course_id) REFERENCES Courses (course_id)
                           );
                       ''')

        # 4. Grades Table
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Grades 
                       (
                       grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       student_id TEXT NOT NULL,
                       assignment_id INTEGER NOT NULL,
                       score INTEGER NOT NULL,
                       FOREIGN KEY (student_id) REFERENCES Students (student_id),
                       FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id) ON DELETE CASCADE,
                       UNIQUE(student_id, assignment_id) -- A student can only have one score per assignment
                           );
                       ''')


        print("Database initialized successfully.")
        conn.commit()
        conn.close()

    def add_student_to_db(self, student_id, first_name, last_name):
        """
        Adds a new student to the Students table.
        Raises an exception if the student ID already exists.
        """
        conn = self.get_db_connection()  # Use self.get_db_connection

        try:
            conn.execute(
                "INSERT INTO Students (student_id, first_name, last_name) VALUES (?, ?, ?)",
                (student_id, first_name, last_name)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Student ID '{student_id}' already exists.")
        except Exception as e:
            conn.close()
            raise e
        finally:
            if conn:
                conn.close()

    def get_all_students(self):
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT student_id, first_name, last_name FROM Students ORDER BY last_name"
            )
            students = cursor.fetchall()
            return students
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []  # Return an empty list on error
        finally:
            if conn:
                conn.close()


    def add_course_to_db(self, course_name, semester):
        conn = self.get_db_connection()
        try:
            conn.execute(
                "INSERT INTO Courses (course_name, course_semester) VALUES (?, ?)",
                (course_name, semester)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Course '{course_name}' in '{semester}' may already exist.")
        except Exception as e:
            conn.close()
            raise e
        finally:
            if conn:
                conn.close()

    def get_all_courses(self):
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT course_id, course_name, course_semester FROM Courses ORDER BY course_name")
            courses = cursor.fetchall()
            return courses
        except Exception as e:
            print(f"Error fetching courses: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def add_assignment_to_db(self, course_id, name, type, max_points):
        """Adds a new assignment to the Assignments table."""
        conn = self.get_db_connection()
        try:
            conn.execute(
                "INSERT INTO Assignments (course_id, assignment_name, assignment_type, max_points) VALUES (?, ?, ?, ?)",
                (course_id, name, type, max_points)
            )
            conn.commit()
        except Exception as e:
            conn.close()
            raise e
        finally:
            if conn:
                conn.close()

    # In database.py (inside the Database class)
    import sqlite3  # Make sure this is imported at the top of the file

    def get_assignments_for_course(self, course_id):
        """Fetches all assignments for a specific course."""
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT assignment_id, assignment_name, max_points FROM Assignments WHERE course_id = ? ORDER BY assignment_name",
                (course_id,)
            )
            assignments = cursor.fetchall()
            return assignments
        except Exception as e:
            print(f"Error fetching assignments: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def add_grade_to_db(self, student_id, assignment_id, score, max_points):
        """
        Adds or updates a grade.
        Fulfills "verify only valid scores"  and "Edits"  requirements.
        """

        # 1. Fulfill "Must verify only valid scores are entered"
        try:
            score_int = int(score)
            if not (0 <= score_int <= max_points):
                raise ValueError(f"Score must be a number between 0 and {max_points}.")
        except ValueError as e:
            # Re-raise the error to be caught by the GUI
            raise ValueError(f"Score must be a whole number between 0 and {max_points}.")

        # 2. Add or Edit the grade.
        # "INSERT OR REPLACE" will add a new row, or
        # replace an existing one if the UNIQUE constraint (student_id, assignment_id) fails.
        # This fulfills the "Edits" requirement.
        conn = self.get_db_connection()
        try:
            conn.execute(
                "INSERT OR REPLACE INTO Grades (student_id, assignment_id, score) VALUES (?, ?, ?)",
                (student_id, assignment_id, score_int)
            )
            conn.commit()
        except Exception as e:
            conn.close()
            raise e
        finally:
            if conn:
                conn.close()

    def get_student_grade_details(self, student_id):
        """
        Fetches a comprehensive list of a student's grades,
        joined with assignment and course details.
        """
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            # This SQL query joins all 4 tables to get the data we need
            sql = """
            SELECT
                C.course_name,
                A.assignment_name,
                A.assignment_type,
                A.max_points,
                G.score,
                S.first_name,
                S.last_name
            FROM Grades G
            JOIN Assignments A ON G.assignment_id = A.assignment_id
            JOIN Courses C ON A.course_id = C.course_id
            JOIN Students S ON G.student_id = S.student_id
            WHERE G.student_id = ?
            ORDER BY C.course_name, A.assignment_type, A.assignment_name
            """
            cursor.execute(sql, (student_id,))
            grades = cursor.fetchall()
            return grades
        except Exception as e:
            print(f"Error fetching grade details: {e}")
            return []
        finally:
            if conn:
                conn.close()

        # In database.py (inside the Database class)

    def delete_assignment(self, assignment_id):
        """Deletes an assignment from the database.
        The ON DELETE CASCADE rule will automatically delete related grades.
        """
        conn = self.get_db_connection()
        try:
            conn.execute("DELETE FROM Assignments WHERE assignment_id = ?", (assignment_id,))
            conn.commit()
        except Exception as e:
            conn.close()
            raise e
        finally:
            if conn:
                conn.close()