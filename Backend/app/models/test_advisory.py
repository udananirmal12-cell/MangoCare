import os
import sys
import joblib


# --------------------------------------------------
# Current folder
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# --------------------------------------------------
# Allow Python to import model_predictor.py
# --------------------------------------------------

if CURRENT_DIR not in sys.path:

    sys.path.insert(
        0,
        CURRENT_DIR
    )


# --------------------------------------------------
# Import prediction function
# --------------------------------------------------

from model_predictor import predict_advisory
from advisory_engine import generate_advisory


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

MODEL_PATH = os.path.join(
    CURRENT_DIR,
    "mango_advisory_model.pkl"
)

package = joblib.load(
    MODEL_PATH
)


print("\n====================================")
print("MANGO AI MODEL TEST")
print("====================================")


# --------------------------------------------------
# Test input
# --------------------------------------------------

test_input = {

    "N": 80,
    "P": 40,
    "K": 50,
    "ph": 6.2,

    "annual_temperature_c": 28.5,
    "annual_rainfall_mm": 1800,
    "annual_et0_mm": 1400,

    "monthly_temperature_c": 29.0,
    "monthly_rainfall_mm": 100,
    "monthly_et0_mm": 120,

    "monthly_wind_max_kmh": 15,
    "monthly_radiation": 20,

    "precipitation_hours": 10,
    "water_balance_mm": -20,

    "elevation": 200,
    "month": 6
}


# --------------------------------------------------
# Prediction
# --------------------------------------------------

prediction = predict_advisory(
    test_input,
    package
)


# --------------------------------------------------
# Display
# --------------------------------------------------

print("\nInput:")
print(test_input)

print("\nAI Prediction:")
print(prediction)

# --------------------------------------------------
# Generate NEW CULTIVATION advisory
# --------------------------------------------------

advisory = generate_advisory(
    mode="new",
    prediction=prediction,
    input_data=test_input
)

# --------------------------------------------------
# Display advisory
# --------------------------------------------------

print("\n====================================")
print("NEW MANGO CULTIVATION ADVISORY")
print("====================================")

print("\nCultivation Suitability:")
print(
    advisory["cultivation_suitability"]
)

print("\nClimate Analysis:")
print(
    advisory["climate_analysis"]
)

print("\nIrrigation Preparation:")
print(
    advisory["irrigation_preparation"]
)

print("\nDrought Alert:")
print(
    advisory["drought_alert"]
)

print("\nNutrient Condition:")
print(
    advisory["nutrient_condition"]
)

print("\nEnvironmental Stress:")
print(
    advisory["environmental_stress"]
)

print("\nRecommendations:")

for recommendation in advisory["recommendations"]:

    print("-", recommendation)