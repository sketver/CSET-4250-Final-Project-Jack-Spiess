# In ViewStudents.py
import tkinter as tk
from tkinter import messagebox


class ViewStudents(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # This map will link the listbox index to the student's ID
        self.student_map = {}

        label = tk.Label(self, text="All Students", font=("Comfortaa", 30), bg="#5cfcff")
        label.pack(pady=20)

        # --- Frame to hold the Listbox and Scrollbar ---
        display_frame = tk.Frame(self)
        display_frame.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(display_frame)
        scrollbar.pack(side="right", fill="y")

        # --- REPLACED Text with Listbox ---
        self.student_listbox = tk.Listbox(
            display_frame,
            font=("Comfortaa", 14),
            yscrollcommand=scrollbar.set
        )
        self.student_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.student_listbox.yview)

        # --- Bind Double-Click to view details (a nice UX touch) ---
        self.student_listbox.bind("<Double-Button-1>", self.on_double_click)

        details_button = tk.Button(
            self,
            text="View Student Grades",
            font=("Comfortaa", 20, "bold"),
            command=self.view_details
        )
        details_button.pack(pady=10)

        button = tk.Button(
            self,
            text="Back to Home",
            font=("Comfortaa", 15, "bold"),
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=10)

    def refresh_data(self):
        self.student_listbox.delete(0, tk.END)
        self.student_map.clear()

        try:
            students = self.controller.db.get_all_students()
            if not students:
                self.student_listbox.insert(tk.END, "No students found.")
            else:
                for i, student in enumerate(students):
                    display_name = f"{student['last_name']}, {student['first_name']} (ID: {student['student_id']})"
                    self.student_listbox.insert(i, display_name)
                    self.student_map[i] = student['student_id']
        except Exception as e:
            self.student_listbox.insert(tk.END, "Error loading students.")
            print(f"Error in ViewStudents refresh_data: {e}")

    def on_double_click(self, event):
        self.view_details()

    def view_details(self):

        try:
            selected_indices = self.student_listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("No Selection", "Please select a student from the list.")
                return

            selected_index = selected_indices[0]

            student_id = self.student_map.get(selected_index)

            if student_id:
                # Save the ID to the controller (App)
                self.controller.current_student_id = student_id
                # Navigate to the detail page
                self.controller.show_frame("StudentDetail")
            else:
                messagebox.showerror("Error", "Could not find student ID for selected item.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")