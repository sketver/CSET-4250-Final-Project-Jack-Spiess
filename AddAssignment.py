# In AddAssignment.py
import tkinter as tk
from tkinter import messagebox


class AddAssignment(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # --- Store courses for the dropdown ---
        self.courses_map = {}  # Stores "Display Name" -> course_id

        label = tk.Label(self, text="Add Assignment", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=20)

        # --- Course Selection Dropdown ---
        label = tk.Label(self, text="Select Course", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)

        self.course_var = tk.StringVar(self)
        self.course_var.set("Loading...")  # Default text
        self.course_menu = tk.OptionMenu(self, self.course_var, "Loading...")
        self.course_menu.config(font=("Comfortaa", 15))
        self.course_menu.pack(pady=10)

        # --- Assignment Type Dropdown ---
        label = tk.Label(self, text="Assignment Type", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)

        self.type_var = tk.StringVar(self)
        self.type_var.set("Homework")  # Default value
        type_options = ["Homework", "Test"]
        type_menu = tk.OptionMenu(self, self.type_var, *type_options)
        type_menu.config(font=("Comfortaa", 15))
        type_menu.pack(pady=10)

        # --- Other Entry Fields ---
        label = tk.Label(self, text="Assignment Name", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.name_entry.pack(pady=10)

        label = tk.Label(self, text="Max Points", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.points_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.points_entry.pack(pady=10)

        # --- Buttons ---
        submit_btn = tk.Button(self, text="Submit", command=self.submit)
        submit_btn.pack(pady=20)

        button = tk.Button(
            self,
            text="Back to Home",
            font=("Comfortaa", 15, "bold"),
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=20)

    def refresh_data(self):
        """Called by show_frame to update the course list."""
        try:
            courses = self.controller.db.get_all_courses()
            self.courses_map.clear()

            if not courses:
                display_options = ["No courses found"]
                self.course_var.set("Add a course first")
            else:
                # Create a user-friendly name and store the ID in our map
                display_options = []
                for course in courses:
                    display_name = f"{course['course_name']} ({course['course_semester']})"
                    display_options.append(display_name)
                    self.courses_map[display_name] = course['course_id']

                self.course_var.set(display_options[0])  # Set default

            # --- Rebuild the OptionMenu ---
            menu = self.course_menu['menu']
            menu.delete(0, 'end')
            for name in display_options:
                menu.add_command(label=name, command=lambda value=name: self.course_var.set(value))

        except Exception as e:
            self.course_var.set("Error loading")
            print(f"Error in refresh_data: {e}")

    def submit(self):
        # 1. Get selected course ID from our map
        selected_name = self.course_var.get()
        course_id = self.courses_map.get(selected_name)

        # 2. Get other values
        assign_type = self.type_var.get()
        assign_name = self.name_entry.get()
        max_points = self.points_entry.get()

        # 3. Validation
        if not course_id:
            messagebox.showerror("Input Error", "Please select a valid course.\n(You may need to add one first).")
            return
        if not assign_name or not max_points:
            messagebox.showerror("Input Error", "Name and Max Points fields must be filled out.")
            return
        try:
            # Validate max_points is an integer
            max_points_int = int(max_points)
        except ValueError:
            messagebox.showerror("Input Error", "Max Points must be a whole number.")
            return

        # 4. Submit to database
        try:
            self.controller.db.add_assignment_to_db(course_id, assign_name, assign_type, max_points_int)
            messagebox.showinfo("Success", f"Assignment '{assign_name}' added to course.")

            # Clear fields
            self.name_entry.delete(0, tk.END)
            self.points_entry.delete(0, tk.END)
            self.type_var.set("Homework")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")