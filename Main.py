import tkinter as tk
from HomePage import HomePage
from AddOrDelete import AddOrDelete
from ViewStudents import ViewStudents
from ShowAdd import ShowAdd
from AddStudent import AddStudent
from database import Database
from AddCourse import AddCourse
from AddAssignment import AddAssignment
from AddGrade import AddGrade
from StudentDetail import StudentDetail
from DeleteAssignment import DeleteAssignment

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Grading App")
        self.geometry("750x750")
        self.config(background="#ffffff")

        self.db = Database("grading.db")

        self.current_student_id = None

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, ViewStudents, AddOrDelete, ShowAdd, AddStudent,
                  AddCourse, AddAssignment, AddGrade, StudentDetail, DeleteAssignment):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage") 

    def show_frame(self, page_name):
        frame = self.frames[page_name]

        if hasattr(frame, "refresh_data"):
            frame.refresh_data()

        frame.tkraise()

print(App)

if __name__ == "__main__":
    app = App()
    app.mainloop()
