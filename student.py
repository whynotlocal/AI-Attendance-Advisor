import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


DATABASE_NAME = "attendance.db"


def register_student(student_id, name, course, semester):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO students
            (student_id, name, course, semester)
            VALUES (?, ?, ?, ?)
        """, (
            student_id,
            name,
            course,
            semester
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Student registered successfully!"
        )

        return True

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Student ID already exists."
        )

        return False

    finally:

        conn.close()


class StudentWindow:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)

        self.window.title("Student Registration")

        self.window.geometry("500x450")

        self.create_form()

    def create_form(self):

        title = tk.Label(
            self.window,
            text="Student Registration",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=20)

        form = tk.Frame(self.window)

        form.pack(pady=10)

        # Student ID

        tk.Label(
            form,
            text="Student ID:"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.student_id = tk.Entry(form, width=30)

        self.student_id.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # Name

        tk.Label(
            form,
            text="Student Name:"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.name = tk.Entry(form, width=30)

        self.name.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        # Course

        tk.Label(
            form,
            text="Course:"
        ).grid(row=2, column=0, padx=10, pady=10)

        self.course = tk.Entry(form, width=30)

        self.course.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )

        # Semester

        tk.Label(
            form,
            text="Semester:"
        ).grid(row=3, column=0, padx=10, pady=10)

        self.semester = ttk.Combobox(
            form,
            values=[1, 2, 3, 4, 5, 6],
            state="readonly",
            width=27
        )

        self.semester.grid(
            row=3,
            column=1,
            padx=10,
            pady=10
        )
        self.semester.current(0)

        # Register button

        register_button = ttk.Button(
            self.window,
            text="Register Student",
            command=self.save_student
        )

        register_button.pack(pady=30)

    def save_student(self):

        student_id = self.student_id.get().strip()
        name = self.name.get().strip()
        course = self.course.get().strip()
        semester = self.semester.get()

        if not student_id or not name:

            messagebox.showwarning(
                "Missing Information",
                "Student ID and Name are required."
            )

            return

        if not course or not semester:

            messagebox.showwarning(
                "Missing Information",
                "Please enter course and semester."
            )

            return

        register_student(
            student_id,
            name,
            course,
            semester
        )