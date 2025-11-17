import tkinter as tk

class ShowAdd(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        button = tk.Button(
            self,
            text="Back to Home",
            font=("Comfortaa", 15, "bold"),
            command=lambda: controller.show_frame("HomePage")
        )
        button.pack(pady=20)