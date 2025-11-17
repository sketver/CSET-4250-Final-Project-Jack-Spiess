# In AddCourse.py
import tkinter as tk
from tkinter import messagebox


class AddCourse(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        label = tk.Label(self, text="Add Course", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=20)

        label = tk.Label(self, text="Course Name (e.g., CSET4250)", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)
        self.name_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.name_entry.pack(pady=10)

        label = tk.Label(self, text="Semester (e.g., Fall 2025)", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)
        self.semester_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.semester_entry.pack(pady=10)

        submit_btn = tk.Button(self, text="Submit", command=self.submit)
        submit_btn.pack(pady=20)

        button = tk.Button(
            self,
            text="Back to Home",
            font=("Comfortaa", 15, "bold"),
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=20)

    def submit(self):
        name = self.name_entry.get()
        semester = self.semester_entry.get()

        if not name or not semester:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            self.controller.db.add_course_to_db(name, semester)
            messagebox.showinfo("Success", f"Course '{name}' added successfully.")

            self.name_entry.delete(0, tk.END)
            self.semester_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")