import tkinter as tk
from HomePage import HomePage
from AddOrDelete import AddOrDelete
from ViewStudents import ViewStudents
from AddStudent import AddStudent
from database import Database
from AddCourse import AddCourse
from AddAssignment import AddAssignment
from AddGrade import AddGrade
from StudentDetail import StudentDetail
from DeleteAssignment import DeleteAssignment
# Basically import every other class so their frames and data can be referenced in this file.

# This initializes the main frame using Tkinter.
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grading App")
        self.geometry("750x750")
        self.config(background="#ffffff")

        # Connects to the database
        self.db = Database("grading.db")

        # Sets the current_student_id variable to none so it does not create errors when referencing new IDs.
        self.current_student_id = None

        # This all designs the look of the GUI
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # This imports all the tkinter frames so they can be shown when buttons are clicked
        for F in (HomePage, ViewStudents, AddOrDelete, AddStudent, AddCourse,
                  AddAssignment, AddGrade, StudentDetail, DeleteAssignment):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage") 

    # This actually shows the different tkinter frame on the gui. It also runs the "refresh_data" function if the class has it.
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "refresh_data"):
            frame.refresh_data()

        frame.tkraise()

# This starts the app
if __name__ == "__main__":
    app = App()
    app.mainloop()
