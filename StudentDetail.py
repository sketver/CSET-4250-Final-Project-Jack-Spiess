# In StudentDetail.py
import tkinter as tk


class StudentDetail(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        self.title_label = tk.Label(self, text="Student Grade Report", font=("Comfortaa", 30), bg="#5cfcff")
        self.title_label.pack(pady=10)

        # --- Frame to hold the grade report ---
        report_frame = tk.Frame(self)
        report_frame.pack(fill="both", expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(report_frame)
        scrollbar.pack(side="right", fill="y")

        self.report_text = tk.Text(
            report_frame,
            font=("Consolas", 12),  # Using a monospaced font helps alignment
            wrap="word",
            state="disabled",
            yscrollcommand=scrollbar.set
        )
        self.report_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.report_text.yview)

        button = tk.Button(
            self,
            text="Back to Student List",
            font=("Comfortaa", 20, "bold"),
            command=lambda: controller.show_frame("ViewStudents")
        )
        button.pack(pady=20)

    def _get_letter_grade(self, percent):
        """Helper function to convert percentage to letter grade."""
        if percent >= 90: return "A"
        if percent >= 80: return "B"
        if percent >= 70: return "C"
        if percent >= 60: return "D"
        return "F"

    def refresh_data(self):
        """
        The main logic. Fetches and processes grade data for
        the selected student.
        """
        # 1. Get the student ID from the controller
        student_id = self.controller.current_student_id
        if not student_id:
            self.title_label.config(text="Error: No Student Selected")
            return

        # 2. Fetch the detailed grade data
        grade_data = self.controller.db.get_student_grade_details(student_id)

        # 3. Enable the text widget for writing
        self.report_text.config(state="normal")
        self.report_text.delete('1.0', tk.END)

        if not grade_data:
            self.title_label.config(text=f"No Grades Found")
            self.report_text.insert(tk.END, "No grades have been entered for this student.")
            self.report_text.config(state="disabled")
            return

        # --- 4. Process the Data (as required by PDF) ---
        student_name = f"{grade_data[0]['first_name']} {grade_data[0]['last_name']}"
        self.title_label.config(text=f"Grade Report for {student_name}")

        report_content = ""
        current_course = None
        hw_scores, hw_max = [], []
        test_scores, test_max = [], []

        for row in grade_data:
            # Check if we are starting a new course block
            if row['course_name'] != current_course:
                # If this isn't the first course, print the summary for the *previous* one
                if current_course is not None:
                    report_content += self._generate_course_summary(
                        current_course, hw_scores, hw_max, test_scores, test_max
                    )

                # Reset for the new course
                current_course = row['course_name']
                hw_scores, hw_max = [], []
                test_scores, test_max = [], []
                report_content += f"\n\n{'=' * 70}\n"
                report_content += f"COURSE: {current_course}\n"
                report_content += f"{'-' * 70}\n"

            # Add the assignment to the correct category
            line_item = f"    {row['assignment_name']} ({row['score']} / {row['max_points']})\n"
            if row['assignment_type'] == 'Homework':
                report_content += line_item
                hw_scores.append(row['score'])
                hw_max.append(row['max_points'])
            elif row['assignment_type'] == 'Test':
                report_content += line_item
                test_scores.append(row['score'])
                test_max.append(row['max_points'])

        # After the loop, print the summary for the *last* course
        report_content += self._generate_course_summary(
            current_course, hw_scores, hw_max, test_scores, test_max
        )

        # 5. Write to text widget and disable editing
        self.report_text.insert('1.0', report_content)
        self.report_text.config(state="disabled")

    def _generate_course_summary(self, course_name, hw_scores, hw_max, test_scores, test_max):
        """Helper method to calculate and format the course summary."""

        summary = f"\n    --- {course_name} Summary ---\n"

        total_hw_score = sum(hw_scores)
        total_hw_max = sum(hw_max)
        hw_percent = (total_hw_score / total_hw_max) * 100 if total_hw_max > 0 else 0
        summary += f"    Homework Total: {total_hw_score} / {total_hw_max}  ({hw_percent:.2f}%)\n"

        total_test_score = sum(test_scores)
        total_test_max = sum(test_max)
        test_percent = (total_test_score / total_test_max) * 100 if total_test_max > 0 else 0
        summary += f"    Test Total:     {total_test_score} / {total_test_max}  ({test_percent:.2f}%)\n"

        # --- Overall Grade Calculation ---
        # NOTE: This assumes HW and Tests are the only categories.
        # You could add weighting here if needed.
        overall_score = total_hw_score + total_test_score
        overall_max = total_hw_max + total_test_max
        overall_percent = (overall_score / overall_max) * 100 if overall_max > 0 else 0
        letter_grade = self._get_letter_grade(overall_percent)

        summary += f"    ---------------------------------------\n"
        summary += f"    OVERALL: {overall_score} / {overall_max}  ({overall_percent:.2f}%) - Grade: {letter_grade}\n"

        return summary