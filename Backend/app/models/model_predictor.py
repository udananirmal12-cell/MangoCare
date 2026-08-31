import pandas as pd


def predict_advisory(input_data, package):

    model = package["model"]
    imputer = package["imputer"]
    encoders = package["target_encoders"]
    features = package["features"]

    # --------------------------------------------------
    # Convert input into DataFrame
    # --------------------------------------------------

    input_df = pd.DataFrame([input_data])

    # --------------------------------------------------
    # Feature engineering
    # --------------------------------------------------

    input_df["temperature_range"] = (
        input_df["annual_temperature_c"]
    )

    input_df["monthly_water_deficit"] = (
        input_df["monthly_et0_mm"]
        -
        input_df["monthly_rainfall_mm"]
    )

    input_df["rainfall_et0_ratio"] = (
        input_df["monthly_rainfall_mm"]
        /
        (input_df["monthly_et0_mm"] + 1e-6)
    )

    input_df["annual_rainfall_et0_ratio"] = (
        input_df["annual_rainfall_mm"]
        /
        (input_df["annual_et0_mm"] + 1e-6)
    )

    input_df["npk_total"] = (
        input_df["N"]
        +
        input_df["P"]
        +
        input_df["K"]
    )

    input_df["npk_balance"] = (
        (input_df["N"] + 1)
        /
        (input_df["P"] + 1)
    )

    input_df["temperature_rainfall_interaction"] = (
        input_df["monthly_temperature_c"]
        *
        input_df["monthly_rainfall_mm"]
    )

    input_df["heat_water_stress_index"] = (
        input_df["monthly_temperature_c"]
        *
        input_df["monthly_et0_mm"]
        /
        (input_df["monthly_rainfall_mm"] + 1)
    )

    # --------------------------------------------------
    # Select features used during training
    # --------------------------------------------------

    X = input_df[features]

    # --------------------------------------------------
    # Apply trained imputer
    # --------------------------------------------------

    X = imputer.transform(X)

    # --------------------------------------------------
    # Random Forest prediction
    # --------------------------------------------------

    prediction = model.predict(X)[0]

    # --------------------------------------------------
    # Decode predictions
    # --------------------------------------------------

    results = {}

    for i, target in enumerate(package["targets"]):

        encoder = encoders[target]

        results[target] = encoder.inverse_transform(
            [prediction[i]]
        )[0]

    return results