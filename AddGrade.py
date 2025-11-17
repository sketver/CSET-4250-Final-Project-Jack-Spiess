# In AddGrade.py
import tkinter as tk
from tkinter import messagebox


class AddGrade(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # --- Dictionaries to map display names back to IDs ---
        self.student_map = {}
        self.course_map = {}
        self.assignment_map = {}  # Will store: name -> (id, max_points)

        label = tk.Label(self, text="Add/Edit Grade", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=10)

        # --- Student Dropdown ---
        label = tk.Label(self, text="Select Student", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.student_var = tk.StringVar(self)
        self.student_menu = tk.OptionMenu(self, self.student_var, "Loading...")
        self.student_menu.config(font=("Comfortaa", 15), width=30)
        self.student_menu.pack(pady=5)

        # --- Course Dropdown ---
        label = tk.Label(self, text="Select Course", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.course_var = tk.StringVar(self)
        self.course_menu = tk.OptionMenu(self, self.course_var, "Loading...")
        self.course_menu.config(font=("Comfortaa", 15), width=30)
        self.course_menu.pack(pady=5)

        # --- Assignment Dropdown (Dependent) ---
        label = tk.Label(self, text="Select Assignment", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.assignment_var = tk.StringVar(self)
        self.assignment_menu = tk.OptionMenu(self, self.assignment_var, "Select course first")
        self.assignment_menu.config(font=("Comfortaa", 15), width=30)
        self.assignment_menu.pack(pady=5)

        # --- Score Entry ---
        self.max_points_label = tk.Label(self, text="Score (Max: --)", font=("Comfortaa", 20), background="#5cfcff")
        self.max_points_label.pack(pady=5)
        self.score_entry = tk.Entry(self, font=("Comfortaa", 20), width=10)
        self.score_entry.pack(pady=5)

        # --- Buttons ---
        submit_btn = tk.Button(self, text="Submit Grade", command=self.submit)
        submit_btn.pack(pady=20)

        back_btn = tk.Button(
            self, text="Back to Home", font=("Comfortaa", 15, "bold"),
            command=lambda: controller.show_frame("HomePage")
        )
        back_btn.pack(pady=10)

        # --- KEY: Link Course Dropdown to Update Assignment Dropdown ---
        # "trace_add" runs a function whenever the variable's value is "written" (changed)
        self.course_var.trace_add("write", self.update_assignment_menu)
        self.assignment_var.trace_add("write", self.update_max_points_label)

    def refresh_data(self):
        """Called by show_frame to update student and course lists."""
        # 1. Populate Students
        try:
            students = self.controller.db.get_all_students()
            self.student_map.clear()
            student_names = ["No students found"]
            if students:
                student_names = []
                for s in students:
                    name = f"{s['last_name']}, {s['first_name']} ({s['student_id']})"
                    student_names.append(name)
                    self.student_map[name] = s['student_id']

            self.student_var.set(student_names[0] if student_names else "Add a student first")
            self.student_menu['menu'].delete(0, 'end')
            for name in student_names:
                self.student_menu['menu'].add_command(label=name, command=lambda v=name: self.student_var.set(v))
        except Exception as e:
            print(f"Error refreshing students: {e}")

        # 2. Populate Courses
        try:
            courses = self.controller.db.get_all_courses()
            self.course_map.clear()
            course_names = ["No courses found"]
            if courses:
                course_names = []
                for c in courses:
                    name = f"{c['course_name']} ({c['course_semester']})"
                    course_names.append(name)
                    self.course_map[name] = c['course_id']

            self.course_var.set(course_names[0] if course_names else "Add a course first")
            self.course_menu['menu'].delete(0, 'end')
            for name in course_names:
                self.course_menu['menu'].add_command(label=name, command=lambda v=name: self.course_var.set(v))
        except Exception as e:
            print(f"Error refreshing courses: {e}")

        # 3. Manually trigger the assignment update for the default course
        self.update_assignment_menu()

    def update_assignment_menu(self, *args):
        """Updates the assignment dropdown based on the selected course."""
        course_name = self.course_var.get()
        course_id = self.course_map.get(course_name)

        self.assignment_map.clear()
        assign_names = ["No assignments found"]

        if course_id:
            try:
                assignments = self.controller.db.get_assignments_for_course(course_id)
                if assignments:
                    assign_names = []
                    for a in assignments:
                        name = f"{a['assignment_name']} ({a['max_points']} pts)"
                        assign_names.append(name)
                        # Store both ID and max_points for validation
                        self.assignment_map[name] = (a['assignment_id'], a['max_points'])
            except Exception as e:
                print(f"Error updating assignments: {e}")

        self.assignment_var.set(assign_names[0] if assign_names else "Add an assignment first")
        self.assignment_menu['menu'].delete(0, 'end')
        for name in assign_names:
            self.assignment_menu['menu'].add_command(label=name, command=lambda v=name: self.assignment_var.set(v))

        # Manually trigger the max points label update
        self.update_max_points_label()

    def update_max_points_label(self, *args):
        """Updates the 'Max Points' label based on the selected assignment."""
        assign_name = self.assignment_var.get()
        data = self.assignment_map.get(assign_name)

        max_points = "--"
        if data:
            max_points = data[1]  # data is (id, max_points)

        self.max_points_label.config(text=f"Score (Max: {max_points})")

    def submit(self):
        # 1. Get all IDs and values
        student_name = self.student_var.get()
        assign_name = self.assignment_var.get()
        score = self.score_entry.get()

        student_id = self.student_map.get(student_name)
        assign_data = self.assignment_map.get(assign_name)

        # 2. Validation
        if not student_id or not assign_data:
            messagebox.showerror("Input Error", "Please select a valid student and assignment.")
            return

        assignment_id, max_points = assign_data

        if not score:
            messagebox.showerror("Input Error", "Please enter a score.")
            return

        # 3. Submit to database (Validation is handled in the DB method)
        try:
            self.controller.db.add_grade_to_db(student_id, assignment_id, score, max_points)
            messagebox.showinfo("Success", f"Grade saved successfully for {student_name}.")

            # Clear score field
            self.score_entry.delete(0, tk.END)

        except ValueError as e:
            # Catches the "invalid score" error we raised in the DB method
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")