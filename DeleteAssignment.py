# In DeleteAssignment.py
import tkinter as tk
from tkinter import messagebox


class DeleteAssignment(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # Maps for our dropdowns
        self.course_map = {}
        self.assignment_map = {}  # Will store: name -> assignment_id

        label = tk.Label(self, text="Delete Assignment", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=20)

        # --- Course Dropdown ---
        label = tk.Label(self, text="Select Course", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.course_var = tk.StringVar(self)
        self.course_menu = tk.OptionMenu(self, self.course_var, "Loading...")
        self.course_menu.config(font=("Comfortaa", 15), width=30)
        self.course_menu.pack(pady=5)

        # --- Assignment Dropdown (Dependent) ---
        label = tk.Label(self, text="Select Assignment to Delete", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.assignment_var = tk.StringVar(self)
        self.assignment_menu = tk.OptionMenu(self, self.assignment_var, "Select course first")
        self.assignment_menu.config(font=("Comfortaa", 15), width=30)
        self.assignment_menu.pack(pady=5)

        # --- Buttons ---
        submit_btn = tk.Button(self, text="Delete Assignment", command=self.submit_delete, bg="red", fg="white",
                               font=("Comfortaa", 15, "bold"))
        submit_btn.pack(pady=20)

        back_btn = tk.Button(
            self, text="Back to Home", font=("Comfortaa", 15, "bold"),
            command=lambda: controller.show_frame("HomePage")
        )
        back_btn.pack(pady=10)

        # Link course dropdown to update assignment dropdown
        self.course_var.trace_add("write", self.update_assignment_menu)

    def refresh_data(self):
        """Called by show_frame to update the course list."""
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

        self.update_assignment_menu()

    def update_assignment_menu(self, *args):
        """Updates the assignment dropdown based on the selected course."""
        course_name = self.course_var.get()
        course_id = self.course_map.get(course_name)

        self.assignment_map.clear()
        assign_names = ["No assignments found"]

        if course_id:
            try:
                # We can reuse this method from AddGrade
                assignments = self.controller.db.get_assignments_for_course(course_id)
                if assignments:
                    assign_names = []
                    for a in assignments:
                        name = f"{a['assignment_name']} ({a['max_points']} pts)"
                        assign_names.append(name)
                        self.assignment_map[name] = a['assignment_id']
            except Exception as e:
                print(f"Error updating assignments: {e}")

        self.assignment_var.set(assign_names[0] if assign_names else "Add an assignment first")
        self.assignment_menu['menu'].delete(0, 'end')
        for name in assign_names:
            self.assignment_menu['menu'].add_command(label=name, command=lambda v=name: self.assignment_var.set(v))

    def submit_delete(self):
        # 1. Get the assignment ID
        assign_name = self.assignment_var.get()
        assignment_id = self.assignment_map.get(assign_name)

        if not assignment_id:
            messagebox.showerror("Selection Error", "Please select a valid assignment to delete.")
            return

        # 2. CRITICAL: Ask for confirmation
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{assign_name}'?\n\n"
            "This will also delete ALL grades entered for this assignment.\n"
            "This action cannot be undone."
        )

        if not confirm:
            return  # User clicked "No"

        # 3. Perform the delete
        try:
            self.controller.db.delete_assignment(assignment_id)
            messagebox.showinfo("Success", f"'{assign_name}' and all its grades have been deleted.")
            # Manually refresh the list
            self.update_assignment_menu()
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")