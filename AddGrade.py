import tkinter as tk
from tkinter import messagebox

# This is for the AddGrade frame
class AddGrade(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # These are dictionaries storing student information for later use
        self.student_map = {}
        self.course_map = {}
        self.assignment_map = {}

        label = tk.Label(self, text="Add/Edit Grade", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=10)

        # This is the student dropdown, it stores your choice as student_var. It also sets the default to loading while it is waiting for data.
        label = tk.Label(self, text="Select Student", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.student_var = tk.StringVar(self)
        self.student_menu = tk.OptionMenu(self, self.student_var, "Loading...")
        self.student_menu.config(font=("Comfortaa", 15), width=30)
        self.student_menu.pack(pady=5)

        # This is the course dropdown, it stores your choice as course_var. It also sets the default to loading while it is waiting for data.
        label = tk.Label(self, text="Select Course", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.course_var = tk.StringVar(self)
        self.course_menu = tk.OptionMenu(self, self.course_var, "Loading...")
        self.course_menu.config(font=("Comfortaa", 15), width=30)
        self.course_menu.pack(pady=5)

        # This is the assignment dropdown, it stores your choice as assignment_var.
        label = tk.Label(self, text="Select Assignment", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.assignment_var = tk.StringVar(self)
        self.assignment_menu = tk.OptionMenu(self, self.assignment_var, "Select course first")
        self.assignment_menu.config(font=("Comfortaa", 15), width=30)
        self.assignment_menu.pack(pady=5)

        # This is the label and entry field for the max points and score.
        self.max_points_label = tk.Label(self, text="Score (Max: --)", font=("Comfortaa", 20), background="#5cfcff")
        self.max_points_label.pack(pady=5)
        self.score_entry = tk.Entry(self, font=("Comfortaa", 20), width=10)
        self.score_entry.pack(pady=5)

        # Submit button calls the submit function.
        submit_btn = tk.Button(self, text="Submit Grade", command=self.submit)
        submit_btn.pack(pady=20)

        # Shows the homepage frame.
        back_btn = tk.Button(
            self, text="Back to Home", font=("Comfortaa", 15, "bold"),
            command=lambda: controller.show_frame("HomePage"))
        back_btn.pack(pady=10)

        # This adds new items to the dropdowns whenever something is added to the database.
        self.course_var.trace_add("write", self.update_assignment_menu)
        self.assignment_var.trace_add("write", self.update_max_points_label)

    # This is called by show_frame to update the dropdowns.
    def refresh_data(self):
        # Adds the students info into the dropdown
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

            # This shows "add a student first" if there are no students.
            self.student_var.set(student_names[0] if student_names else "Add a student first")
            self.student_menu['menu'].delete(0, 'end')
            for name in student_names:
                self.student_menu['menu'].add_command(label=name, command=lambda v=name: self.student_var.set(v))
        except Exception as e:
            print(f"Error refreshing students: {e}")

        # Adds the courses info into the dropdown
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

            # This shows "add a course first" if there are no courses found.
            self.course_var.set(course_names[0] if course_names else "Add a course first")
            self.course_menu['menu'].delete(0, 'end')
            for name in course_names:
                self.course_menu['menu'].add_command(label=name, command=lambda v=name: self.course_var.set(v))
        except Exception as e:
            print(f"Error refreshing courses: {e}")

        # Automatically update the assignments for the default course by calling the update_assignment_menu function.
        self.update_assignment_menu()

    # This function updates the info in the assignments dropdown depending on the selected course.
    def update_assignment_menu(self, *args):
        # Gets the course selected and maps it.
        course_name = self.course_var.get()
        course_id = self.course_map.get(course_name)

        # This shows "No assignments found" if there are no assignments for the course selected.
        self.assignment_map.clear()
        assign_names = ["No assignments found"]

        # This looks to see if there are assignments using the get_assignments_for_course function with the course_id parameter.
        if course_id:
            try:
                assignments = self.controller.db.get_assignments_for_course(course_id)
                # If there are assignments, this stores them.
                if assignments:
                    assign_names = []
                    for a in assignments:
                        name = f"{a['assignment_name']} ({a['max_points']} pts)"
                        assign_names.append(name)
                        # This stores both ID and max_points for validation
                        self.assignment_map[name] = (a['assignment_id'], a['max_points'])
            except Exception as e:
                print(f"Error updating assignments: {e}")

        # This sees if there is an assignment and reads "add an assignment first" if there isn't one.
        self.assignment_var.set(assign_names[0] if assign_names else "Add an assignment first")
        self.assignment_menu['menu'].delete(0, 'end')
        for name in assign_names:
            self.assignment_menu['menu'].add_command(label=name, command=lambda v=name: self.assignment_var.set(v))

        # Automatically trigger the max points label update by calling the update_max_points_label function.
        self.update_max_points_label()

    # This function shows the max points in the menu as part of the max_points_label
    def update_max_points_label(self, *args):
        assign_name = self.assignment_var.get()
        data = self.assignment_map.get(assign_name)

        max_points = "--"
        # This shows the 1 value of the assignment variable (id=0 and max_points=1). It replaces the two dashes with the max points.
        if data:
            max_points = data[1]

        self.max_points_label.config(text=f"Score (Max: {max_points})")

    def submit(self):
        # This gets all the ids and values and stores them.
        student_name = self.student_var.get()
        assign_name = self.assignment_var.get()
        score = self.score_entry.get()

        student_id = self.student_map.get(student_name)
        assign_data = self.assignment_map.get(assign_name)

        # If there is not a student id or assign_data variable stored it throws an error.
        if not student_id or not assign_data:
            messagebox.showerror("Input Error", "Please select a valid student and assignment.")
            return

        assignment_id, max_points = assign_data

        # If there is no score stored it throws an error.
        if not score:
            messagebox.showerror("Input Error", "Please enter a score.")
            return

        # Call the add_grade_to_db function and add it to the database.
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