# AI Attendance Advisor

An AI-based attendance management system developed using Python and Tkinter. The system helps students and administrators monitor daily attendance, calculate attendance percentages, predict examination eligibility, and identify attendance risk using Machine Learning.

## 📌 Project Overview

The AI Attendance Advisor is designed to make attendance monitoring easier and more intelligent.

Instead of manually calculating attendance percentages, the system records daily subject-wise attendance and automatically calculates attendance statistics.

The system also uses a Machine Learning model to predict attendance risk and provides recommendations based on the student's attendance performance.

## ✨ Features

### 👨‍🎓 Student Management
- Register students
- Store student information
- Select course
- Select semester
- Support for 6 semesters
- View registered students

### 📚 Subject Management
- Add subjects
- Assign subjects to courses and semesters
- View available subjects

### 📝 Daily Attendance
- Select course
- Select semester
- Select student
- Select subject
- Select attendance date
- Mark Present or Absent
- Save daily attendance
- Update attendance for an existing date

### 📊 Attendance Analysis
- Automatically calculate total classes
- Calculate attended classes
- Calculate absent classes
- Calculate attendance percentage
- Subject-wise attendance monitoring

### 🤖 Machine Learning Prediction
- Predict attendance risk
- Classify students as:
  - LOW
  - MEDIUM
  - HIGH
- Display prediction confidence
- Use attendance-related features for prediction

### ⚠️ Attendance Advisor
- Examination eligibility prediction
- Attendance warnings
- Personalized recommendations
- Helps students understand how many classes they need to attend

### 📄 Attendance Reports
- View attendance records
- View subject-wise attendance
- Monitor attendance performance

## 🧠 Machine Learning

The system uses a Decision Tree Classifier to predict attendance risk.

### Input Features

The model uses:

- Attendance Percentage
- Total Classes
- Attended Classes
- Absent Classes
- Recent Attendance Percentage

### Risk Levels

| Attendance | Risk |
|------------|------|
| 75% and above | LOW |
| 65% – 74% | MEDIUM |
| Below 65% | HIGH |

The Machine Learning model is trained using `train_model.py`.

The trained model is saved as:

```text
attendance_risk_model.pkl
