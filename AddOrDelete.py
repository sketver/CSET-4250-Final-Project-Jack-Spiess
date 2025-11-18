# Import tkinter for gui
import tkinter as tk

# This is where you choose if you want to add, delete, or edit courses, students, and grades.
class AddOrDelete(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # Tkinter label that says "Add or Delete"
        label = (tk.Label (self, text="Add or Delete", font=("Comfortaa", 30), background="#5cfcff"))
        label.pack(pady=20)

        # Tkinter button that reads "Add a Student" and shows the "AddStudent" frame.
        button = tk.Button(self, text="Add a Student", font=("Comfortaa", 20, "bold"),
                           command=lambda: controller.show_frame("AddStudent"))
        button.pack(pady=20)

        # Tkinter button that reads "Add a Course" and shows the "AddCourses" frame.
        button = tk.Button(self, text="Add a Course", font=("Comfortaa", 20, "bold"),
                           command=lambda: controller.show_frame("AddCourse"))
        button.pack(pady=20)

        # Tkinter button that reads "Add an Assignment" and shows the "AddAssignment" frame.
        button = tk.Button(self, text="Add an Assignment", font=("Comfortaa", 20, "bold"),
                           command=lambda: controller.show_frame("AddAssignment"))
        button.pack(pady=20)

        # Tkinter button that reads "Add/Edit a Grade" and shows the "AddAssignment" frame.
        button = tk.Button(self, text="Add/Edit a Grade", font=("Comfortaa", 20, "bold"),
                           command=lambda: controller.show_frame("AddGrade"))
        button.pack(pady=20)

        # Tkinter button that reads "Delete an Assignment" and shows the "DeleteAssignment" frame.
        button = tk.Button(self, text="Delete an Assignment", font=("Comfortaa", 20, "bold"),
                           command=lambda: controller.show_frame("DeleteAssignment"))
        button.pack(pady=20)

        # Tkinter button that reads "Back to Home" and takes you back to the "HomePage" Frame.
        button = tk.Button(self, text="Back to Home", font=("Comfortaa", 15, "bold"),
                           command=lambda: controller.show_frame("HomePage"))
        button.pack(pady=20)
