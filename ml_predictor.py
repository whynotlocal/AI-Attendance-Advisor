import os
import joblib


MODEL_PATH = "attendance_risk_model.pkl"


def predict_risk(
    attendance_percentage,
    total_classes,
    attended_classes,
    absent_classes,
    recent_percentage
):

    # Check model

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "ML model not found.\n\n"
            "Please run:\n"
            "python train_model.py"
        )

    # Load model

    model = joblib.load(
        MODEL_PATH
    )

    # Prepare input

    features = [[

        attendance_percentage,

        total_classes,

        attended_classes,

        absent_classes,

        recent_percentage

    ]]

    # Prediction

    prediction = model.predict(
        features
    )[0]

    # Probability

    probabilities = model.predict_proba(
        features
    )[0]

    classes = model.classes_

    confidence = max(
        probabilities
    ) * 100

    return {

        "risk": prediction,

        "confidence": confidence

    }