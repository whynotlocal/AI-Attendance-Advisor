import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from advisor import predict_eligibility


DATABASE_NAME = "attendance.db"


class ReportWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Attendance Report")
        self.window.geometry("950x600")

        self.window.resizable(False, False)

        self.create_interface()

    def create_interface(self):

        # Title

        title = tk.Label(
            self.window,
            text="Attendance Report",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=20)

        # Search frame

        search_frame = tk.Frame(
            self.window
        )

        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Student ID:",
            font=("Arial", 11)
        ).grid(
            row=0,
            column=0,
            padx=10
        )

        self.student_id = tk.Entry(
            search_frame,
            width=30
        )

        self.student_id.grid(
            row=0,
            column=1,
            padx=10
        )

        search_button = ttk.Button(
            search_frame,
            text="Generate Report",
            command=self.generate_report
        )

        search_button.grid(
            row=0,
            column=2,
            padx=10
        )

        # Student information

        self.student_info = tk.Label(
            self.window,
            text="",
            font=("Arial", 12, "bold")
        )

        self.student_info.pack(
            pady=10
        )

        # Table frame

        table_frame = tk.Frame(
            self.window
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        columns = (
            "subject",
            "total",
            "present",
            "absent",
            "percentage",
            "status",
            "risk"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.table.heading(
            "subject",
            text="Subject"
        )

        self.table.heading(
            "total",
            text="Total"
        )

        self.table.heading(
            "present",
            text="Present"
        )

        self.table.heading(
            "absent",
            text="Absent"
        )

        self.table.heading(
            "percentage",
            text="Attendance %"
        )

        self.table.heading(
            "status",
            text="Eligibility"
        )

        self.table.heading(
            "risk",
            text="Risk"
        )

        self.table.column(
            "subject",
            width=200
        )

        self.table.column(
            "total",
            width=80,
            anchor="center"
        )

        self.table.column(
            "present",
            width=80,
            anchor="center"
        )

        self.table.column(
            "absent",
            width=80,
            anchor="center"
        )

        self.table.column(
            "percentage",
            width=110,
            anchor="center"
        )

        self.table.column(
            "status",
            width=130,
            anchor="center"
        )

        self.table.column(
            "risk",
            width=100,
            anchor="center"
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

    def generate_report(self):

        student_id = self.student_id.get().strip()

        if not student_id:

            messagebox.showwarning(
                "Missing Information",
                "Please enter Student ID."
            )

            return

        conn = sqlite3.connect(
            DATABASE_NAME
        )

        cursor = conn.cursor()

        # Get student

        cursor.execute(
            """
            SELECT student_id, name, course, semester
            FROM students
            WHERE student_id = ?
            """,
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:

            conn.close()

            messagebox.showerror(
                "Student Not Found",
                "No student found with this Student ID."
            )

            return

        # Display student information

        self.student_info.config(
            text=(
                f"Student: {student[1]}    |    "
                f"ID: {student[0]}    |    "
                f"Course: {student[2]}    |    "
                f"Semester: {student[3]}"
            )
        )

        # Get subjects

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

        # Clear old table

        for item in self.table.get_children():

            self.table.delete(item)

        if not subjects:

            messagebox.showinfo(
                "No Attendance",
                "No attendance records found."
            )

            return

        # Process each subject

        for subject in subjects:

            conn = sqlite3.connect(
                DATABASE_NAME
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    SUM(
                        CASE
                            WHEN status = 'Present'
                            THEN 1
                            ELSE 0
                        END
                    )
                FROM attendance
                WHERE student_id = ?
                AND subject = ?
                """,
                (
                    student_id,
                    subject
                )
            )

            result = cursor.fetchone()

            conn.close()

            total = result[0] or 0

            present = result[1] or 0

            absent = total - present

            prediction = predict_eligibility(
                present,
                total
            )

            self.table.insert(
                "",
                "end",
                values=(
                    subject,
                    total,
                    present,
                    absent,
                    f"{prediction['percentage']:.2f}%",
                    prediction["status"],
                    prediction["risk"]
                )
            )