import tkinter as tk
from tkinter import messagebox

# This class is used to draw the frame to add assignments to the database.
class AddAssignment(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # Stores the courses for the dropdown later
        self.courses_map = {}

        label = tk.Label(self, text="Add Assignment", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=20)

        # This is a label that reads "Select Course"
        label = tk.Label(self, text="Select Course", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)

        # This creates the dropdown and automatically sets it to "Loading..." until it has loaded and able to show courses.
        self.course_var = tk.StringVar(self)
        self.course_var.set("Loading...")
        self.course_menu = tk.OptionMenu(self, self.course_var, "Loading...")
        self.course_menu.config(font=("Comfortaa", 15))
        self.course_menu.pack(pady=10)

        # This is the label for the Assignment Type dropdown
        label = tk.Label(self, text="Assignment Type", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)

        # This is the assignment type dropdown, with it automatically being set to homework, with the other option being test.
        self.type_var = tk.StringVar(self)
        self.type_var.set("Homework")
        type_options = ["Homework", "Test"]
        # Stores the selected option as type_var
        type_menu = tk.OptionMenu(self, self.type_var, *type_options)
        type_menu.config(font=("Comfortaa", 15))
        type_menu.pack(pady=10)

        # Label and entry field for the assignment name.
        label = tk.Label(self, text="Assignment Name", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.name_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.name_entry.pack(pady=10)

        # Label and entry fields for the number of points allowed.
        label = tk.Label(self, text="Max Points", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=5)
        self.points_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.points_entry.pack(pady=10)

        # This tkinter button calls the submit function.
        submit_btn = tk.Button(self, text="Submit",
                               command=self.submit)
        submit_btn.pack(pady=20)

        # This tkinter button takes you back home
        button = tk.Button(self, text="Back to Home", font=("Comfortaa", 15, "bold"),
                           command=lambda: controller.show_frame("HomePage"))
        button.pack(pady=20)

    # This function refreshes the data in the courses database to account for any changes.
    def refresh_data(self):
        try:
            # Calls the get_all_courses function
            courses = self.controller.db.get_all_courses()
            self.courses_map.clear()

            # If the function does not provide any courses, display "Add a course first"
            if not courses:
                display_options = ["No courses found"]
                self.course_var.set("Add a course first")
            else:
                # Create a user-friendly name and store the ID in the map created earlier. It also sets the default
                display_options = []
                for course in courses:
                    display_name = f"{course['course_name']} ({course['course_semester']})"
                    display_options.append(display_name)
                    self.courses_map[display_name] = course['course_id']

                self.course_var.set(display_options[0])

            # This builds the new data in the course_menu dropdown after refresh
            menu = self.course_menu['menu']
            menu.delete(0, 'end')
            for name in display_options:
                menu.add_command(label=name, command=lambda value=name: self.course_var.set(value))

        except Exception as e:
            self.course_var.set("Error loading")
            print(f"Error in refresh_data: {e}")

    def submit(self):
        # This gets the selected course from the map
        selected_name = self.course_var.get()
        course_id = self.courses_map.get(selected_name)

        # This gets the other value from the fields and type dropdown
        assign_type = self.type_var.get()
        assign_name = self.name_entry.get()
        max_points = self.points_entry.get()

        # This shows an error if there is no course_id, assign_name, or max_points fields.
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

        # Calls the add_assignment_to_db function to add it to the database.
        try:
            self.controller.db.add_assignment_to_db(course_id, assign_name, assign_type, max_points_int)
            messagebox.showinfo("Success", f"Assignment '{assign_name}' added to course.")

            # Clear fields
            self.name_entry.delete(0, tk.END)
            self.points_entry.delete(0, tk.END)
            self.type_var.set("Homework")

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")