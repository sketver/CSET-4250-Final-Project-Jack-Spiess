import tkinter as tk

# This is shown when you are looking at the students grades.
class StudentDetail(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(background="#5cfcff")

        # Tkinter label that reads "Student Grade Report"
        self.title_label = tk.Label(self, text="Student Grade Report", font=("Comfortaa", 30), bg="#5cfcff")
        self.title_label.pack(pady=10)

        # This is the frame to hold the report.
        report_frame = tk.Frame(self)
        report_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # This puts a scrollbar on the right side of that frame.
        scrollbar = tk.Scrollbar(report_frame)
        scrollbar.pack(side="right", fill="y")

        # Sets the font and style of the report.
        self.report_text = tk.Text(report_frame, font=("Consolas", 12), wrap="word",
                                   state="disabled", yscrollcommand=scrollbar.set)
        self.report_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.report_text.yview)

        # This takes you to the ViewStudents frame so you can look at other students.
        button = tk.Button(self, text="Back to Student List", font=("Comfortaa", 20, "bold"),
                           command=lambda: controller.show_frame("ViewStudents"))
        button.pack(pady=20)

    def _get_letter_grade(self, percent):
        # This converts the percentage to a letter grade.
        if percent >= 90: return "A"
        if percent >= 80: return "B"
        if percent >= 70: return "C"
        if percent >= 60: return "D"
        return "F"

    # References and shows the data for a selected student.
    def refresh_data(self):
        # Gets the data from the controller
        student_id = self.controller.current_student_id
        if not student_id:
            self.title_label.config(text="Error: No Student Selected")
            return

        # Grabs the grade data for the students using the get_student_grade_details function.
        grade_data = self.controller.db.get_student_grade_details(student_id)

        # This allows the frame to write the data
        self.report_text.config(state="normal")
        self.report_text.delete('1.0', tk.END)

        # Shows errors if there is a problem getting the grade data.
        if not grade_data:
            self.title_label.config(text=f"No Grades Found")
            self.report_text.insert(tk.END, "No grades have been entered for this student.")
            self.report_text.config(state="disabled")
            return

        # Creates a variable called student_name from the grade_data and shows it with a label at the top.
        student_name = f"{grade_data[0]['first_name']} {grade_data[0]['last_name']}"
        self.title_label.config(text=f"Grade Report for {student_name}")

        # Creates data to be filled later, it also establishes separate hw and test groups.
        report_content = ""
        current_course = None
        hw_scores, hw_max = [], []
        test_scores, test_max = [], []


        for row in grade_data:
            # Check if we are starting a new course block
            if row['course_name'] != current_course:
                # If this isn't the first course, print the summary for the last one
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

        # After the loop, print the summary for the last course
        report_content += self._generate_course_summary(
            current_course, hw_scores, hw_max, test_scores, test_max
        )

        # 5. Write to text widget and disable editing
        self.report_text.insert('1.0', report_content)
        self.report_text.config(state="disabled")

    # This helps calculate and format the summary
    def _generate_course_summary(self, course_name, hw_scores, hw_max, test_scores, test_max):
        summary = f"\n    --- {course_name} Summary ---\n"

        # Adds the scores and calculates the percentage for homework
        total_hw_score = sum(hw_scores)
        total_hw_max = sum(hw_max)
        hw_percent = (total_hw_score / total_hw_max) * 100 if total_hw_max > 0 else 0
        summary += f"    Homework Total: {total_hw_score} / {total_hw_max}  ({hw_percent:.2f}%)\n"

        # Adds the scores and calculates the percentage for tests
        total_test_score = sum(test_scores)
        total_test_max = sum(test_max)
        test_percent = (total_test_score / total_test_max) * 100 if total_test_max > 0 else 0
        summary += f"    Test Total:     {total_test_score} / {total_test_max}  ({test_percent:.2f}%)\n"

        # Adds the hw and test scores together, divides them by the max possible and call _get_letter_grade function using the overall_percent parameter.
        overall_score = total_hw_score + total_test_score
        overall_max = total_hw_max + total_test_max
        overall_percent = (overall_score / overall_max) * 100 if overall_max > 0 else 0
        letter_grade = self._get_letter_grade(overall_percent)

        # Just some formatting to make it clearer between grades
        summary += f"    ---------------------------------------\n"
        # Shows the percentage, how many points you got, and the letter grade.
        summary += f"    OVERALL: {overall_score} / {overall_max}  ({overall_percent:.2f}%) - Grade: {letter_grade}\n"

        return summary