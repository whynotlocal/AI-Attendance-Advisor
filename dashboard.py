import tkinter as tk
from tkinter import ttk
import sqlite3

from advisor import predict_eligibility


DATABASE_NAME = "attendance.db"


class Dashboard:

    def __init__(self, parent):

        self.parent = parent

        self.frame = tk.Frame(
            parent,
            bg="#f4f6f8"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.create_dashboard()

    def create_dashboard(self):

        # ---------------- TITLE ----------------

        title_frame = tk.Frame(
            self.frame,
            bg="#f4f6f8"
        )

        title_frame.pack(
            fill="x",
            padx=30,
            pady=(20, 10)
        )

        title = tk.Label(
            title_frame,
            text="Attendance Dashboard",
            font=("Arial", 22, "bold"),
            bg="#f4f6f8"
        )

        title.pack(
            anchor="w"
        )

        subtitle = tk.Label(
            title_frame,
            text="Monitor attendance and examination eligibility",
            font=("Arial", 11),
            bg="#f4f6f8",
            fg="#555555"
        )

        subtitle.pack(
            anchor="w",
            pady=5
        )

        # ---------------- STATISTICS ----------------

        stats_frame = tk.Frame(
            self.frame,
            bg="#f4f6f8"
        )

        stats_frame.pack(
            fill="x",
            padx=30,
            pady=15
        )

        self.total_card = self.create_card(
            stats_frame,
            "Total Students",
            "0",
            0
        )

        self.eligible_card = self.create_card(
            stats_frame,
            "Eligible",
            "0",
            1
        )

        self.risk_card = self.create_card(
            stats_frame,
            "At Risk",
            "0",
            2
        )

        self.not_eligible_card = self.create_card(
            stats_frame,
            "Not Eligible",
            "0",
            3
        )

        # ---------------- AVERAGE ----------------

        average_frame = tk.Frame(
            self.frame,
            bg="white",
            relief="groove",
            borderwidth=1
        )

        average_frame.pack(
            fill="x",
            padx=30,
            pady=10
        )

        tk.Label(
            average_frame,
            text="Average Attendance",
            font=("Arial", 14, "bold"),
            bg="white"
        ).pack(
            pady=(15, 5)
        )

        self.average_label = tk.Label(
            average_frame,
            text="0.00%",
            font=("Arial", 24, "bold"),
            bg="white"
        )

        self.average_label.pack(
            pady=(0, 15)
        )

        # ---------------- WARNING SECTION ----------------

        warning_title = tk.Label(
            self.frame,
            text="Attendance Warnings",
            font=("Arial", 16, "bold"),
            bg="#f4f6f8"
        )

        warning_title.pack(
            anchor="w",
            padx=30,
            pady=(15, 5)
        )

        warning_frame = tk.Frame(
            self.frame,
            bg="white",
            relief="groove",
            borderwidth=1
        )

        warning_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 20)
        )

        self.warning_list = tk.Listbox(
            warning_frame,
            font=("Arial", 11),
            height=8,
            borderwidth=0
        )

        self.warning_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Load data

        self.load_statistics()

    # ------------------------------------------------
    # CREATE STATISTIC CARD
    # ------------------------------------------------

    def create_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = tk.Frame(
            parent,
            bg="white",
            relief="groove",
            borderwidth=1,
            width=180,
            height=100
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 10),
            bg="white",
            fg="#555555"
        ).pack(
            pady=(15, 5)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 22, "bold"),
            bg="white"
        )

        value_label.pack()

        return value_label

    # ------------------------------------------------
    # LOAD STATISTICS
    # ------------------------------------------------

    def load_statistics(self):

        conn = sqlite3.connect(
            DATABASE_NAME
        )

        cursor = conn.cursor()

        # Total students

        cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        total_students = cursor.fetchone()[0]

        # Get all students

        cursor.execute(
            """
            SELECT student_id, name
            FROM students
            """
        )

        students = cursor.fetchall()

        conn.close()

        eligible = 0
        at_risk = 0
        not_eligible = 0

        attendance_values = []

        warnings = []

        for student_id, name in students:

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
                """,
                (student_id,)
            )

            result = cursor.fetchone()

            conn.close()

            total = result[0] or 0

            present = result[1] or 0

            if total == 0:
                continue

            prediction = predict_eligibility(
                present,
                total
            )

            percentage = prediction["percentage"]

            attendance_values.append(
                percentage
            )

            status = prediction["status"]

            if status == "ELIGIBLE":

                eligible += 1

            elif status == "AT RISK":

                at_risk += 1

            elif status == "NOT ELIGIBLE":

                not_eligible += 1

            # Warning

            if percentage < 75:

                warnings.append(
                    f"{student_id} - {name}: "
                    f"{percentage:.2f}% attendance "
                    f"({status})"
                )

        # Update cards

        self.total_card.config(
            text=str(total_students)
        )

        self.eligible_card.config(
            text=str(eligible)
        )

        self.risk_card.config(
            text=str(at_risk)
        )

        self.not_eligible_card.config(
            text=str(not_eligible)
        )

        # Average attendance

        if attendance_values:

            average = (
                sum(attendance_values)
                / len(attendance_values)
            )

        else:

            average = 0

        self.average_label.config(
            text=f"{average:.2f}%"
        )

        # Warnings

        self.warning_list.delete(
            0,
            tk.END
        )

        if warnings:

            for warning in warnings:

                self.warning_list.insert(
                    tk.END,
                    "⚠ " + warning
                )

        else:

            self.warning_list.insert(
                tk.END,
                "✓ No attendance warnings."
            )

    def refresh(self):

        self.load_statistics()