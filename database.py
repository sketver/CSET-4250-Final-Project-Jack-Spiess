import sqlite3


class Database:
    def __init__(self, db_file):
        # This constructor stores the database file and use the initialize_database function to create the database.
        self.db_file = db_file
        self.initialize_database()

    def get_db_connection(self):
        # This function creates the connection to the database for the other functions in this class to use.
        conn = sqlite3.connect(self.db_file)
        # This allows for the easier use and display of the database.
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_database(self):
        # This function initializes and actually runs the sql scripts to create the database.
        conn = self.get_db_connection()  # Use self.get_db_connection
        cursor = conn.cursor()

        # Creates the students table using sql code in quotations.
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Students
                       (
                           student_id TEXT PRIMARY KEY,
                           first_name TEXT NOT NULL,
                           last_name TEXT NOT NULL
                       );
                       ''')
        # Creates the courses table using sql code in quotations
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Courses
                       (
                           course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           course_name TEXT NOT NULL,
                           course_semester TEXT NOT NULL
                       );
                       ''')

        # Creates the assignments table using sql code in quotations
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

        # Creates a grades table using the sql code in the quotations.
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS Grades 
                       (
                       grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       student_id TEXT NOT NULL,
                       assignment_id INTEGER NOT NULL,
                       score INTEGER NOT NULL,
                       FOREIGN KEY (student_id) REFERENCES Students (student_id),
                       FOREIGN KEY (assignment_id) REFERENCES Assignments (assignment_id) ON DELETE CASCADE,
                       UNIQUE(student_id, assignment_id)
                           );
                       ''')

        # Commits and closes the changes to the database and closes it.
        conn.commit()
        conn.close()

    # This function is called when a new student is added to the database and adds the student. It also raises an error if the student ID is already in use.
    def add_student_to_db(self, student_id, first_name, last_name):
        conn = self.get_db_connection()

        try:
            # This takes the parameters of student_id, first_name, and last_name and inserts into the Students table.
            conn.execute(
                "INSERT INTO Students (student_id, first_name, last_name) VALUES (?, ?, ?)",
                (student_id, first_name, last_name)
            )
            conn.commit()
        # This displays a "Student with this ID already exists" error, as well as shows an error if anything else unexpected happens.
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Student ID '{student_id}' already exists.")
        except Exception as e:
            conn.close()
            raise e
        finally:
            if conn:
                conn.close()

    # This function gets all the students and shows them when called.
    def get_all_students(self):
        conn = self.get_db_connection()
        # This returns all the students and orders them by last name.
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT student_id, first_name, last_name FROM Students ORDER BY last_name"
            )
            students = cursor.fetchall()
            return students
        # This returns an empty list with "Error fetching students"
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []
        finally:
            if conn:
                conn.close()

    # This function adds courses to the database.
    def add_course_to_db(self, course_name, semester):
        conn = self.get_db_connection()
        # Takes parameters and inserts them into the grading database.
        try:
            conn.execute(
                "INSERT INTO Courses (course_name, course_semester) VALUES (?, ?)",
                (course_name, semester)
            )
            conn.commit()
        # This raises an error if the course already exists in that semester.
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Course '{course_name}' in '{semester}' may already exist.")
        except Exception as e:
            conn.close()
            raise e
        finally:
            if conn:
                conn.close()

    # This gets all the courses in the database and is called when someone wants to add a grade.
    def get_all_courses(self):
        conn = self.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT course_id, course_name, course_semester FROM Courses ORDER BY course_name")
            courses = cursor.fetchall()
            return courses
        # Throws an error if they can't get the courses.
        except Exception as e:
            print(f"Error fetching courses: {e}")
            return []
        finally:
            if conn:
                conn.close()

    # This function is to be called when an assignment is added to the database
    def add_assignment_to_db(self, course_id, name, type, max_points):
        conn = self.get_db_connection()
        # Takes the parameters of course_id, name, type, and max_points and adds it as an assignment
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

    # Gets all the assignments for a specific course.
    def get_assignments_for_course(self, course_id):
        conn = self.get_db_connection()
        # This query takes assignments tied to a specific course and shows them.
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

    # Adds the grades to the database and ties them to a specific student.
    def add_grade_to_db(self, student_id, assignment_id, score, max_points):
        # Stores the score as an int, and raises an error if it is not between 0 and the max points for the assignments, as well as if it is not a whole number.
        try:
            score_int = int(score)
            if not (0 <= score_int <= max_points):
                raise ValueError(f"Score must be a number between 0 and {max_points}.")
        except ValueError as e:
            # Re-raise the error to be caught by the GUI
            raise ValueError(f"Score must be a whole number between 0 and {max_points}.")

        # This adds or edits grades in the database
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

    # Gets a list of all a students grades
    def get_student_grade_details(self, student_id):
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
        # Shows an error when something goes wrong.
        except Exception as e:
            print(f"Error fetching grade details: {e}")
            return []
        finally:
            if conn:
                conn.close()

    # Deletes an assignment from the database, and uses the delete cascades to delete other related items.
    def delete_assignment(self, assignment_id):

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