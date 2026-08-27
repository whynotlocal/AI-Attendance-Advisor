import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from attendance_calculator import get_attendance, get_recent_attendance
from advisor import predict_eligibility
from ml_predictor import predict_risk


DATABASE_NAME = "attendance.db"


class PredictionWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("AI Attendance Advisor - Eligibility Prediction")
        self.window.geometry("750x750")
        self.window.resizable(False, False)

        self.create_interface()


    # =========================================================
    # CREATE INTERFACE
    # =========================================================

    def create_interface(self):

        title = tk.Label(
            self.window,
            text="AI Attendance Advisor",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(20, 5))


        subtitle = tk.Label(
            self.window,
            text="Examination Eligibility Prediction",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 20))


        # -----------------------------------------------------
        # INPUT FRAME
        # -----------------------------------------------------

        input_frame = tk.Frame(
            self.window
        )
        input_frame.pack(pady=10)


        # Student ID

        tk.Label(
            input_frame,
            text="Student ID",
            font=("Arial", 11, "bold")
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )


        self.student_id = tk.Entry(
            input_frame,
            width=30,
            font=("Arial", 11)
        )

        self.student_id.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )


        # Subject

        tk.Label(
            input_frame,
            text="Subject",
            font=("Arial", 11, "bold")
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )


        self.subject = ttk.Combobox(
            input_frame,
            width=28,
            state="readonly"
        )

        self.subject.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )


        # Load Subjects Button

        ttk.Button(
            input_frame,
            text="Load Subjects",
            command=self.load_subject_button
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=10
        )


        # Predict Button

        predict_button = tk.Button(
            self.window,
            text="Predict Eligibility",
            font=("Arial", 12, "bold"),
            command=self.predict,
            padx=20,
            pady=8
        )

        predict_button.pack(
            pady=10
        )


        # -----------------------------------------------------
        # RESULT FRAME
        # -----------------------------------------------------

        self.result_frame = tk.Frame(
            self.window,
            relief="groove",
            borderwidth=2
        )

        self.result_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )


    # =========================================================
    # LOAD SUBJECTS
    # =========================================================

    def load_subjects(self, student_id):

        conn = sqlite3.connect(
            DATABASE_NAME
        )

        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT DISTINCT subject
            FROM attendance
            WHERE student_id = ?
            ORDER BY subject
            """,
            (student_id,)
        )


        subjects = [
            row[0]
            for row in cursor.fetchall()
        ]


        conn.close()


        self.subject["values"] = subjects


        return subjects


    # =========================================================
    # LOAD SUBJECT BUTTON
    # =========================================================

    def load_subject_button(self):

        student_id = self.student_id.get().strip()


        if not student_id:

            messagebox.showwarning(
                "Missing Student ID",
                "Please enter the Student ID first."
            )

            return


        subjects = self.load_subjects(
            student_id
        )


        if not subjects:

            messagebox.showwarning(
                "No Subjects Found",
                "No attendance records were found "
                "for this student."
            )

            return


        self.subject.current(0)


        messagebox.showinfo(
            "Subjects Loaded",
            f"{len(subjects)} subject(s) loaded."
        )


    # =========================================================
    # PREDICT ELIGIBILITY
    # =========================================================

    def predict(self):

        student_id = self.student_id.get().strip()


        if not student_id:

            messagebox.showwarning(
                "Missing Student ID",
                "Please enter the Student ID."
            )

            return


        # Load subjects automatically if necessary

        subjects = self.load_subjects(
            student_id
        )


        if not subjects:

            messagebox.showwarning(
                "No Attendance Data",
                "No attendance records were found "
                "for this student."
            )

            return


        # Select first subject automatically

        if not self.subject.get():

            self.subject.current(0)


        subject = self.subject.get().strip()


        if not subject:

            messagebox.showwarning(
                "Missing Subject",
                "Please select a subject."
            )

            return


        # -----------------------------------------------------
        # GET ATTENDANCE
        # -----------------------------------------------------

        attendance = get_attendance(
            student_id,
            subject
        )


        total = attendance["total"]

        present = attendance["present"]

        absent = attendance["absent"]


        if total == 0:

            messagebox.showwarning(
                "No Attendance",
                "No attendance records are available "
                "for this subject."
            )

            return


        # -----------------------------------------------------
        # CALCULATE ELIGIBILITY
        # -----------------------------------------------------

        result = predict_eligibility(
            present,
            total
        )


        # -----------------------------------------------------
        # RECENT ATTENDANCE
        # -----------------------------------------------------

        recent_percentage = get_recent_attendance(
            student_id,
            subject
        )


        # -----------------------------------------------------
        # MACHINE LEARNING PREDICTION
        # -----------------------------------------------------

        try:

            ml_result = predict_risk(
                attendance_percentage=result["percentage"],
                total_classes=total,
                attended_classes=present,
                absent_classes=absent,
                recent_percentage=recent_percentage
            )


        except FileNotFoundError:

            messagebox.showerror(
                "ML Model Not Found",
                "The trained ML model was not found.\n\n"
                "Please run:\n"
                "python train_model.py"
            )

            return


        except Exception as error:

            messagebox.showerror(
                "ML Prediction Error",
                f"An error occurred:\n\n{error}"
            )

            return


        # -----------------------------------------------------
        # DISPLAY RESULT
        # -----------------------------------------------------

        self.display_result(
            student_id,
            subject,
            attendance,
            result,
            recent_percentage,
            ml_result
        )


    # =========================================================
    # DISPLAY RESULT
    # =========================================================

    def display_result(
        self,
        student_id,
        subject,
        attendance,
        result,
        recent_percentage,
        ml_result
    ):

        # Remove old results

        for widget in self.result_frame.winfo_children():

            widget.destroy()


        # -----------------------------------------------------
        # STUDENT INFORMATION
        # -----------------------------------------------------

        tk.Label(
            self.result_frame,
            text=f"Student ID: {student_id}",
            font=("Arial", 12, "bold")
        ).pack(
            pady=4
        )


        tk.Label(
            self.result_frame,
            text=f"Subject: {subject}",
            font=("Arial", 12)
        ).pack(
            pady=4
        )


        # -----------------------------------------------------
        # ATTENDANCE DETAILS
        # -----------------------------------------------------

        details_frame = tk.Frame(
            self.result_frame
        )

        details_frame.pack(
            pady=8
        )


        tk.Label(
            details_frame,
            text=f"Total Classes: {attendance['total']}",
            font=("Arial", 11)
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=3
        )


        tk.Label(
            details_frame,
            text=f"Present: {attendance['present']}",
            font=("Arial", 11)
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=3
        )


        tk.Label(
            details_frame,
            text=f"Absent: {attendance['absent']}",
            font=("Arial", 11)
        ).grid(
            row=0,
            column=2,
            padx=20,
            pady=3
        )


        # -----------------------------------------------------
        # ATTENDANCE PERCENTAGE
        # -----------------------------------------------------

        tk.Label(
            self.result_frame,
            text=f"{result['percentage']:.2f}%",
            font=("Arial", 25, "bold")
        ).pack(
            pady=5
        )


        tk.Label(
            self.result_frame,
            text="Current Attendance",
            font=("Arial", 11)
        ).pack()


        tk.Label(
            self.result_frame,
            text="Minimum Required: 75%",
            font=("Arial", 11)
        ).pack(
            pady=5
        )


        # -----------------------------------------------------
        # ELIGIBILITY
        # -----------------------------------------------------

        tk.Label(
            self.result_frame,
            text=f"Eligibility: {result['status']}",
            font=("Arial", 15, "bold")
        ).pack(
            pady=8
        )


        # -----------------------------------------------------
        # RISK
        # -----------------------------------------------------

        tk.Label(
            self.result_frame,
            text=f"Attendance Risk: {result['risk']}",
            font=("Arial", 12, "bold")
        ).pack(
            pady=3
        )


        # -----------------------------------------------------
        # REQUIRED CLASSES
        # -----------------------------------------------------

        if result["required_classes"] > 0:

            tk.Label(
                self.result_frame,
                text=(
                    f"Classes required to reach 75%: "
                    f"{result['required_classes']}"
                ),
                font=("Arial", 11, "bold")
            ).pack(
                pady=5
            )

        else:

            tk.Label(
                self.result_frame,
                text="Attendance requirement satisfied.",
                font=("Arial", 11)
            ).pack(
                pady=5
            )


        # -----------------------------------------------------
        # RECENT ATTENDANCE
        # -----------------------------------------------------

        tk.Label(
            self.result_frame,
            text=(
                f"Recent Attendance: "
                f"{recent_percentage:.2f}%"
            ),
            font=("Arial", 11)
        ).pack(
            pady=5
        )


        # -----------------------------------------------------
        # ML PREDICTION
        # -----------------------------------------------------

        ml_frame = tk.LabelFrame(
            self.result_frame,
            text="AI / ML Prediction",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )

        ml_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )


        tk.Label(
            ml_frame,
            text=(
                f"Predicted Risk: "
                f"{ml_result['risk']}"
            ),
            font=("Arial", 12, "bold")
        ).pack(
            pady=3
        )


        tk.Label(
            ml_frame,
            text=(
                f"Model Confidence: "
                f"{ml_result['confidence']:.2f}%"
            ),
            font=("Arial", 11)
        ).pack(
            pady=3
        )


        # -----------------------------------------------------
        # ADVISOR RECOMMENDATION
        # -----------------------------------------------------

        advisor_frame = tk.LabelFrame(
            self.result_frame,
            text="AI Advisor Recommendation",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8
        )

        advisor_frame.pack(
            fill="x",
            padx=30,
            pady=5
        )


        tk.Label(
            advisor_frame,
            text=result["message"],
            font=("Arial", 10),
            wraplength=620,
            justify="center"
        ).pack(
            pady=5
        )