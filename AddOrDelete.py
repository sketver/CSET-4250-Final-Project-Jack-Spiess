
# Import tkinter for gui
import tkinter as tk

class AddOrDelete(tk.Frame):
    #
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        label = (tk.Label
                 (self,
                  text="Add or Delete Students",
                  font=("Comfortaa", 30),
                  background="#5cfcff"
                  )
                 )
        label.pack(pady=20)

        button = tk.Button(
            self,
            text="Add a Student",
            font=("Comfortaa", 20, "bold"),
            command=lambda: controller.show_frame("AddStudent")
        )
        button.pack(pady=20)

        button = tk.Button(
            self,
            text="Add a Course",
            font=("Comfortaa", 20, "bold"),
            command=lambda: controller.show_frame("AddCourse") # placeholder
        )
        button.pack(pady=20)

        button = tk.Button(
            self,
            text="Add an Assignment",  # <--- Renamed button
            font=("Comfortaa", 20, "bold"),
            command=lambda: controller.show_frame("AddAssignment")  # <--- Changed command
        )
        button.pack(pady=20)

        button = tk.Button(
            self,
            text="Add/Edit a Grade",
            font=("Comfortaa", 20, "bold"),
            command=lambda: controller.show_frame("AddGrade")
        )
        button.pack(pady=20)

        button = tk.Button(
            self,
            text="Delete an Assignment",
            font=("Comfortaa", 20, "bold"),
            command=lambda: controller.show_frame("DeleteAssignment")
        )
        button.pack(pady=20)

        button = tk.Button(
            self,
            text="Back to Home",
            font=("Comfortaa", 15, "bold"),
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=20)
