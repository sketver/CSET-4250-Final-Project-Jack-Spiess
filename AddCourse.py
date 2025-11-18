# In AddCourse.py
import tkinter as tk
from tkinter import messagebox


class AddCourse(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # Tkinter label reading add course
        label = tk.Label(self, text="Add Course", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=20)

        # Tkinter label and entry field for Course Name with the example of CSET4250. Stores entry as name_entry
        label = tk.Label(self, text="Course Name (e.g., CSET4250)", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)
        self.name_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.name_entry.pack(pady=10)

        # Tkinter label and entry field for the semester with the example of fall 2025. Stores entry as semester_entry.
        label = tk.Label(self, text="Semester (e.g., Fall 2025)", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)
        self.semester_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.semester_entry.pack(pady=10)

        # Tkinter button calling the submit function.
        submit_btn = tk.Button(self, text="Submit", command=self.submit)
        submit_btn.pack(pady=20)

        # Tkinter button taking you to the HomePage Frame.
        button = tk.Button(self, text="Back to Home", font=("Comfortaa", 15, "bold"),
                           command=lambda: controller.show_frame("HomePage"))
        button.pack(pady=20)

    def submit(self):
        name = self.name_entry.get()
        semester = self.semester_entry.get()

        # Throws an error if name or semester is blank
        if not name or not semester:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        # Adds the course using the add_course_to_db function with the name and semester parameters and shows a success box.
        try:
            self.controller.db.add_course_to_db(name, semester)
            messagebox.showinfo("Success", f"Course '{name}' added successfully.")

            # Clears the fields.
            self.name_entry.delete(0, tk.END)
            self.semester_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")