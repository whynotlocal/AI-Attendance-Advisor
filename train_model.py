import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

import joblib


# ==================================================
# CREATE TRAINING DATA
# ==================================================

np.random.seed(42)

data = []

for _ in range(1000):

    total_classes = np.random.randint(20, 101)

    attendance_percentage = np.random.uniform(
        40,
        100
    )

    attended_classes = round(
        total_classes *
        attendance_percentage /
        100
    )

    absent_classes = (
        total_classes -
        attended_classes
    )

    recent_percentage = np.clip(
        attendance_percentage +
        np.random.uniform(-15, 15),
        0,
        100
    )

    # Risk classification

    if attendance_percentage >= 75:

        risk = "LOW"

    elif attendance_percentage >= 65:

        risk = "MEDIUM"

    else:

        risk = "HIGH"

    data.append([
        attendance_percentage,
        total_classes,
        attended_classes,
        absent_classes,
        recent_percentage,
        risk
    ])


# ==================================================
# CREATE DATAFRAME
# ==================================================

columns = [
    "attendance_percentage",
    "total_classes",
    "attended_classes",
    "absent_classes",
    "recent_percentage",
    "risk"
]

df = pd.DataFrame(
    data,
    columns=columns
)


print("\nTraining Dataset:")
print(df.head())

print(
    "\nNumber of records:",
    len(df)
)


# ==================================================
# FEATURES
# ==================================================

X = df[
    [
        "attendance_percentage",
        "total_classes",
        "attended_classes",
        "absent_classes",
        "recent_percentage"
    ]
]


# ==================================================
# TARGET
# ==================================================

y = df["risk"]


# ==================================================
# TRAIN / TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


# ==================================================
# CREATE MODEL
# ==================================================

model = DecisionTreeClassifier(

    max_depth=5,

    random_state=42
)


# ==================================================
# TRAIN
# ==================================================

model.fit(
    X_train,
    y_train
)


# ==================================================
# TEST
# ==================================================

predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    "\nModel Accuracy:",
    f"{accuracy * 100:.2f}%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# ==================================================
# SAVE MODEL
# ==================================================

joblib.dump(
    model,
    "attendance_risk_model.pkl"
)


print(
    "\nModel saved successfully!"
)

print(
    "File: attendance_risk_model.pkl"
)