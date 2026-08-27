import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


DATABASE_NAME = "attendance.db"


class AttendanceWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Attendance Entry")

        self.window.geometry("550x450")

        self.window.resizable(False, False)

        self.create_form()

    def create_form(self):

        title = tk.Label(
            self.window,
            text="Attendance Entry",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=20)

        form = tk.Frame(self.window)

        form.pack(pady=10)

        # Student ID

        tk.Label(
            form,
            text="Student ID:"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.student_id = tk.Entry(
            form,
            width=30
        )

        self.student_id.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # Subject

        tk.Label(
            form,
            text="Subject:"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.subject = tk.Entry(
            form,
            width=30
        )

        self.subject.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        # Date

        tk.Label(
            form,
            text="Date:"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.date_entry = tk.Entry(
            form,
            width=30
        )

        self.date_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        self.date_entry.insert(
            0,
            date.today().strftime("%Y-%m-%d")
        )

        # Attendance status

        tk.Label(
            form,
            text="Attendance:"
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.status = ttk.Combobox(
            form,
            values=["Present", "Absent"],
            state="readonly",
            width=27
        )

        self.status.grid(
            row=3,
            column=1,
            padx=10,
            pady=10
        )

        self.status.current(0)

        # Save button

        save_button = ttk.Button(
            self.window,
            text="Save Attendance",
            command=self.save_attendance
        )

        save_button.pack(pady=30)

    def save_attendance(self):

        student_id = self.student_id.get().strip()

        subject = self.subject.get().strip()

        attendance_date = self.date_entry.get().strip()

        status = self.status.get()

        # Validate fields

        if not student_id:

            messagebox.showwarning(
                "Missing Information",
                "Please enter Student ID."
            )

            return

        if not subject:

            messagebox.showwarning(
                "Missing Information",
                "Please enter Subject."
            )

            return

        if not attendance_date:

            messagebox.showwarning(
                "Missing Information",
                "Please enter Date."
            )

            return

        if not status:

            messagebox.showwarning(
                "Missing Information",
                "Please select attendance status."
            )

            return

        # Connect database

        conn = sqlite3.connect(DATABASE_NAME)

        cursor = conn.cursor()

        # Check student

        cursor.execute(
            """
            SELECT *
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
                "Please register this student first."
            )

            return

        # Prevent duplicate attendance

        cursor.execute(
            """
            SELECT *
            FROM attendance
            WHERE student_id = ?
            AND subject = ?
            AND date = ?
            """,
            (
                student_id,
                subject,
                attendance_date
            )
        )

        existing_record = cursor.fetchone()

        if existing_record:

            conn.close()

            messagebox.showwarning(
                "Duplicate Attendance",
                "Attendance for this student, subject and date "
                "has already been recorded."
            )

            return

        # Insert attendance

        cursor.execute(
            """
            INSERT INTO attendance
            (
                student_id,
                subject,
                date,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                student_id,
                subject,
                attendance_date,
                status
            )
        )

        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            f"Attendance saved successfully!\n\n"
            f"Student ID: {student_id}\n"
            f"Subject: {subject}\n"
            f"Status: {status}"
        )

        # Clear fields

        self.subject.delete(0, tk.END)

        self.date_entry.delete(0, tk.END)

        self.date_entry.insert(
            0,
            date.today().strftime("%Y-%m-%d")
        )

        self.status.current(0)