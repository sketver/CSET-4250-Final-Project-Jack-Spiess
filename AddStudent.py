import tkinter as tk
from tkinter import messagebox


class AddStudent(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        label = tk.Label(self, text="Add Student", font=("Comfortaa", 30), background="#5cfcff")
        label.pack(pady=10)

        label = tk.Label(self, text="First Name", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)

        self.f_name_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.f_name_entry.pack(pady=10)

        label = tk.Label(self, text="Last Name", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)

        self.l_name_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.l_name_entry.pack(pady=10)

        label = tk.Label(self, text="ID", font=("Comfortaa", 20), background="#5cfcff")
        label.pack(pady=10)

        self.stu_id_entry = tk.Entry(self, font=("Comfortaa", 20))
        self.stu_id_entry.pack(pady=10)

        submit_btn = tk.Button(self, text="Submit", command=self.submit, font=("Comfortaa", 20))
        submit_btn.pack(pady=10)

        button = tk.Button(self, text="Back to Home", font=("Comfortaa", 15, "bold"), command=lambda: controller.show_frame("HomePage"))
        button.pack(pady=20)


    def submit(self):
        first = self.f_name_entry.get()
        last = self.l_name_entry.get()
        s_id = self.stu_id_entry.get()

        if not first or not last or not s_id:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        try:
            self.controller.db.add_student_to_db(s_id, first, last)

            messagebox.showinfo("Success", f"Student {first} {last} added successfully.")

            self.f_name_entry.delete(0, tk.END)
            self.l_name_entry.delete(0, tk.END)
            self.stu_id_entry.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Database Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")