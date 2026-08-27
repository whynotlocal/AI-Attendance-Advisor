import tkinter as tk
from tkinter import ttk

from database import create_database

from student import StudentWindow
from attendance import AttendanceWindow
from prediction import PredictionWindow
from report import ReportWindow

from dashboard import Dashboard


class AttendanceAdvisorApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AI Attendance Advisor"
        )

        self.root.geometry(
            "1000x700"
        )

        self.root.resizable(
            False,
            False
        )

        create_database()

        self.create_header()

        self.create_navigation()

        self.dashboard = Dashboard(
            self.root
        )

    # ------------------------------------------------
    # HEADER
    # ------------------------------------------------

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#1f4e79",
            height=70
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="AI Attendance Advisor",
            font=("Arial", 22, "bold"),
            bg="#1f4e79",
            fg="white"
        )

        title.pack(
            side="left",
            padx=25,
            pady=18
        )

    # ------------------------------------------------
    # NAVIGATION
    # ------------------------------------------------

    def create_navigation(self):

        navigation = tk.Frame(
            self.root,
            bg="#e9edf2",
            height=50
        )

        navigation.pack(
            fill="x"
        )

        dashboard_button = ttk.Button(
            navigation,
            text="Dashboard",
            command=self.show_dashboard
        )

        dashboard_button.pack(
            side="left",
            padx=8,
            pady=8
        )

        student_button = ttk.Button(
            navigation,
            text="Student Registration",
            command=lambda:
                StudentWindow(self.root)
        )

        student_button.pack(
            side="left",
            padx=8,
            pady=8
        )

        attendance_button = ttk.Button(
            navigation,
            text="Attendance Entry",
            command=lambda:
                AttendanceWindow(self.root)
        )

        attendance_button.pack(
            side="left",
            padx=8,
            pady=8
        )

        prediction_button = ttk.Button(
            navigation,
            text="Eligibility Prediction",
            command=lambda:
                PredictionWindow(self.root)
        )

        prediction_button.pack(
            side="left",
            padx=8,
            pady=8
        )

        report_button = ttk.Button(
            navigation,
            text="Attendance Report",
            command=lambda:
                ReportWindow(self.root)
        )

        report_button.pack(
            side="left",
            padx=8,
            pady=8
        )

    # ------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------

    def show_dashboard(self):

        # Remove current dashboard

        if hasattr(
            self,
            "dashboard"
        ):

            self.dashboard.frame.destroy()

        self.dashboard = Dashboard(
            self.root
        )


if __name__ == "__main__":

    root = tk.Tk()

    app = AttendanceAdvisorApp(
        root
    )

    root.mainloop()