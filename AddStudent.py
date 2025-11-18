import tkinter as tk
from tkinter import messagebox

# This is used when you want to add a student.
class AddStudent(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # Tkinter label that reads "Add Student"
        label = tk.Label(self, text="Add Student", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=10)

        # Tkinter label that reads "First Name"
        label = tk.Label(self, text="First Name", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)

        # Tkinter entry field called f_name_entry
        self.f_name_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.f_name_entry.pack(pady=10)

        # Tkinter label that reads "Last Name"
        label = tk.Label(self, text="Last Name", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)

        # Tkinter entry field called l_name_entry
        self.l_name_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.l_name_entry.pack(pady=10)

        # Tkinter label that reads "ID"
        label = tk.Label(self, text="ID", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)

        # Tkinter entry field called stu_id_entry
        self.stu_id_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.stu_id_entry.pack(pady=10)

        # Submit button
        submit_btn = tk.Button(self, text="Submit", command=self.submit, font=("Comfortaa", 20))
        submit_btn.pack(pady=10)

        # Button that takes you back to the home page
        button = tk.Button(self, text="Back to Home", font=("Comfortaa", 15, "bold"),
                           command=lambda: controller.show_frame("HomePage"))
        button.pack(pady=20)

    # This function is called when the submit button is pressed.
    def submit(self):
        # This creates variables from the entry fields and calls them first, last, and s_id.
        first = self.f_name_entry.get()
        last = self.l_name_entry.get()
        s_id = self.stu_id_entry.get()

        # This shows an error if one of the entry fields is not filled out.
        if not first or not last or not s_id:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        # This adds the student to the database and shows a message box saying success. It calls the function add_student_to_db from the database class to do it.
        try:
            self.controller.db.add_student_to_db(s_id, first, last)

            messagebox.showinfo("Success", f"Student {first} {last} added successfully.")

            # This clears out the Entry fields from earlier.
            self.f_name_entry.delete(0, tk.END)
            self.l_name_entry.delete(0, tk.END)
            self.stu_id_entry.delete(0, tk.END)

        # This shows an error if it can't access the database
        except ValueError as e:
            messagebox.showerror("Database Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")