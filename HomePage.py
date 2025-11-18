import tkinter as tk

# This is the page that loads when you load the application
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # Tkinter label that says "Welcome to my grading app."
        hello_label = tk.Label(self, text="Welcome to my grading app.", font=("Comfortaa", 30), bg="#5cfcff")
        hello_label.pack(pady=20)

        # Tkinter button that shows the "ViewStudents" frame.
        view_button = tk.Button(self, text="View Students", font=("Comfortaa", 25, "bold"),
                                command=lambda: controller.show_frame("ViewStudents"))
        view_button.pack(pady=10)

        # Tkinter button that shows " Add or Drop Grades and Courses."
        add_button = tk.Button(self, text="Add or Drop Grades and Courses", font=("Comfortaa", 25, "bold"),
                               command=lambda: controller.show_frame("AddOrDelete"))
        add_button.pack(pady=10)
