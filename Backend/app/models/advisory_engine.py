

def _safe_float(value, default=0.0):
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ============================================================
# 1. CLIMATE ANALYSIS
# ============================================================

def analyze_climate(input_data):

    temperature = _safe_float(
        input_data.get("annual_temperature_c")
    )

    rainfall = _safe_float(
        input_data.get("annual_rainfall_mm")
    )

    elevation = _safe_float(
        input_data.get("elevation")
    )

    ph = _safe_float(
        input_data.get("ph")
    )

    details = []

    # --------------------------------------------------------
    # Temperature
    # --------------------------------------------------------

    if 27 <= temperature <= 30:

        temperature_status = "Suitable"

    elif 25 <= temperature <= 32:

        temperature_status = "Moderately Suitable"

        details.append(
            "Annual temperature is moderately suitable "
            "for mango cultivation."
        )

    else:

        temperature_status = "Less Suitable"

        details.append(
            "Annual temperature may not be ideal "
            "for mango cultivation."
        )

    # --------------------------------------------------------
    # Rainfall
    # --------------------------------------------------------

    if 500 <= rainfall <= 2500:

        rainfall_status = "Suitable"

    elif 300 <= rainfall <= 3000:

        rainfall_status = "Moderately Suitable"

        details.append(
            "Annual rainfall may require additional "
            "water management."
        )

    else:

        rainfall_status = "Less Suitable"

        details.append(
            "Annual rainfall conditions may be unsuitable "
            "for mango cultivation."
        )

    # --------------------------------------------------------
    # Elevation
    # --------------------------------------------------------

    if elevation <= 600:

        elevation_status = "Suitable"

    elif elevation <= 800:

        elevation_status = "Moderately Suitable"

        details.append(
            "Elevation is relatively high and should "
            "be considered when planning cultivation."
        )

    else:

        elevation_status = "Less Suitable"

        details.append(
            "Elevation may be unsuitable for the "
            "planned mango cultivation."
        )

    # --------------------------------------------------------
    # Soil pH
    # --------------------------------------------------------

    if 5.5 <= ph <= 7.5:

        soil_ph_status = "Suitable"

    elif 5.0 <= ph <= 8.0:

        soil_ph_status = "Moderately Suitable"

        details.append(
            "Soil pH may require management before "
            "establishing mango cultivation."
        )

    else:

        soil_ph_status = "Less Suitable"

        details.append(
            "Soil pH is outside the preferred range "
            "used by this advisory system."
        )

    # --------------------------------------------------------
    # Overall climate status
    # --------------------------------------------------------

    statuses = [
        temperature_status,
        rainfall_status,
        elevation_status,
        soil_ph_status
    ]

    if all(
        status == "Suitable"
        for status in statuses
    ):

        overall_status = "Suitable"

    elif "Less Suitable" in statuses:

        overall_status = "Needs Attention"

    else:

        overall_status = "Moderately Suitable"

    return {

        "temperature_status":
            temperature_status,

        "rainfall_status":
            rainfall_status,

        "elevation_status":
            elevation_status,

        "soil_ph_status":
            soil_ph_status,

        "overall_climate_status":
            overall_status,

        "details":
            details
    }


# ============================================================
# 2. IRRIGATION ADVISORY
# ============================================================

def generate_irrigation_advisory(
    prediction,
    input_data
):

    irrigation_prediction = str(
        prediction.get(
            "irrigation_need",
            "Moderate"
        )
    ).lower()

    rainfall = _safe_float(
        input_data.get(
            "monthly_rainfall_mm"
        )
    )

    et0 = _safe_float(
        input_data.get(
            "monthly_et0_mm"
        )
    )

    water_deficit = et0 - rainfall

    # --------------------------------------------------------
    # High irrigation
    # --------------------------------------------------------

    if irrigation_prediction == "high":

        return {

            "level": "High",

            "title":
                "High Irrigation Requirement",

            "message":
                "The analysed conditions indicate a high "
                "irrigation requirement.",

            "action":
                "Prepare adequate water resources and "
                "closely monitor soil moisture.",

            "water_deficit_mm":
                round(water_deficit, 2)
        }

    # --------------------------------------------------------
    # Moderate irrigation
    # --------------------------------------------------------

    elif irrigation_prediction == "moderate":

        return {

            "level": "Moderate",

            "title":
                "Moderate Irrigation Requirement",

            "message":
                "Supplementary irrigation may be required "
                "during periods of insufficient rainfall.",

            "action":
                "Monitor rainfall, water availability "
                "and soil moisture.",

            "water_deficit_mm":
                round(water_deficit, 2)
        }

    # --------------------------------------------------------
    # Low irrigation
    # --------------------------------------------------------

    else:

        return {

            "level": "Low",

            "title":
                "Low Irrigation Requirement",

            "message":
                "The analysed conditions indicate a "
                "relatively low irrigation requirement.",

            "action":
                "Continue normal rainfall and soil-moisture monitoring.",

            "water_deficit_mm":
                round(water_deficit, 2)
        }


# ============================================================
# 3. DROUGHT ADVISORY
# ============================================================

def generate_drought_advisory(
    prediction,
    input_data
):

    drought_prediction = str(
        prediction.get(
            "drought_risk",
            "Low"
        )
    ).lower()

    rainfall = _safe_float(
        input_data.get(
            "monthly_rainfall_mm"
        )
    )

    et0 = _safe_float(
        input_data.get(
            "monthly_et0_mm"
        )
    )

    # --------------------------------------------------------
    # High
    # --------------------------------------------------------

    if drought_prediction == "high":

        return {

            "level": "High",

            "alert": True,

            "title":
                "High Drought Risk",

            "message":
                "High drought risk is indicated under "
                "the analysed conditions.",

            "action":
                "Increase water-management preparedness "
                "and closely monitor soil moisture.",

            "rainfall_mm":
                rainfall,

            "et0_mm":
                et0
        }

    # --------------------------------------------------------
    # Moderate
    # --------------------------------------------------------

    elif drought_prediction == "moderate":

        return {

            "level": "Moderate",

            "alert": True,

            "title":
                "Moderate Drought Risk",

            "message":
                "Moderate drought risk is indicated.",

            "action":
                "Monitor rainfall, soil moisture and "
                "water availability closely.",

            "rainfall_mm":
                rainfall,

            "et0_mm":
                et0
        }

    # --------------------------------------------------------
    # Low
    # --------------------------------------------------------

    else:

        return {

            "level": "Low",

            "alert": False,

            "title":
                "Low Drought Risk",

            "message":
                "No significant drought risk is indicated "
                "under the analysed conditions.",

            "action":
                "Continue normal environmental monitoring.",

            "rainfall_mm":
                rainfall,

            "et0_mm":
                et0
        }


# ============================================================
# 4. NUTRIENT ADVISORY
# ============================================================

def generate_nutrient_advisory(
    prediction,
    input_data
):

    nutrient_prediction = str(
        prediction.get(
            "nutrient_condition",
            "Deficient"
        )
    ).lower()

    n = _safe_float(
        input_data.get("N")
    )

    p = _safe_float(
        input_data.get("P")
    )

    k = _safe_float(
        input_data.get("K")
    )

    # --------------------------------------------------------
    # Deficient
    # --------------------------------------------------------

    if nutrient_prediction == "deficient":

        return {

            "status": "Deficient",

            "priority": "High",

            "message":
                "The predicted nutrient condition "
                "requires attention.",

            "action":
                "Conduct soil testing before applying "
                "fertilizer.",

            "N": n,
            "P": p,
            "K": k
        }

    # --------------------------------------------------------
    # Adequate
    # --------------------------------------------------------

    elif nutrient_prediction == "adequate":

        return {

            "status": "Adequate",

            "priority": "Low",

            "message":
                "The predicted nutrient condition "
                "is currently adequate.",

            "action":
                "Continue regular soil and nutrient monitoring.",

            "N": n,
            "P": p,
            "K": k
        }

    # --------------------------------------------------------
    # Other / moderate condition
    # --------------------------------------------------------

    else:

        return {

            "status":
                prediction.get(
                    "nutrient_condition"
                ),

            "priority": "Medium",

            "message":
                "The nutrient condition should be monitored.",

            "action":
                "Consider soil testing before making "
                "fertilizer decisions.",

            "N": n,
            "P": p,
            "K": k
        }


# ============================================================
# 5. ENVIRONMENTAL STRESS
# ============================================================

def analyze_environmental_stress(
    prediction,
    input_data
):

    temperature = _safe_float(
        input_data.get(
            "monthly_temperature_c"
        )
    )

    rainfall = _safe_float(
        input_data.get(
            "monthly_rainfall_mm"
        )
    )

    et0 = _safe_float(
        input_data.get(
            "monthly_et0_mm"
        )
    )

    wind = _safe_float(
        input_data.get(
            "monthly_wind_max_kmh"
        )
    )

    stress_factors = []

    # Temperature stress
    if temperature >= 32:

        stress_factors.append(
            "High monthly temperature"
        )

    # Water stress
    if rainfall < et0:

        stress_factors.append(
            "Monthly rainfall is below "
            "estimated evapotranspiration"
        )

    # Wind stress
    if wind >= 35:

        stress_factors.append(
            "High maximum monthly wind speed"
        )

    # Drought
    drought = str(
        prediction.get(
            "drought_risk",
            "Low"
        )
    ).lower()

    if drought in ["moderate", "high"]:

        stress_factors.append(
            f"{prediction['drought_risk']} drought risk"
        )

    # Determine overall level
    if len(stress_factors) >= 2:

        level = "High"

    elif len(stress_factors) == 1:

        level = "Moderate"

    else:

        level = "Low"

    return {

        "level":
            level,

        "factors":
            stress_factors
    }


# ============================================================
# 6. WEATHER / DISEASE RISK INDICATION
# ============================================================
#
# IMPORTANT:
# This is NOT a disease ML model.
# It is an environmental-risk rule.
#
# A proper disease prediction model can be added later
# if disease-labelled data becomes available.
# ============================================================

def generate_disease_risk_advisory(
    input_data
):

    temperature = _safe_float(
        input_data.get(
            "monthly_temperature_c"
        )
    )

    rainfall = _safe_float(
        input_data.get(
            "monthly_rainfall_mm"
        )
    )

    precipitation_hours = _safe_float(
        input_data.get(
            "precipitation_hours"
        )
    )

    risk_factors = []

    # Wet conditions
    if rainfall >= 150:

        risk_factors.append(
            "High monthly rainfall"
        )

    # Frequent wet periods
    if precipitation_hours >= 15:

        risk_factors.append(
            "Frequent precipitation conditions"
        )

    # Warm + wet environment
    if (
        temperature >= 24
        and rainfall >= 150
    ):

        risk_factors.append(
            "Warm and wet environmental conditions"
        )

    if len(risk_factors) >= 2:

        risk = "High"

        message = (
            "Environmental conditions may be favourable "
            "for some mango disease development. "
            "Increase crop monitoring."
        )

    elif len(risk_factors) == 1:

        risk = "Moderate"

        message = (
            "Some environmental conditions may favour "
            "disease development. Monitor plants regularly."
        )

    else:

        risk = "Low"

        message = (
            "No strong environmental disease-risk "
            "indicators were detected."
        )

    return {

        "risk_level":
            risk,

        "message":
            message,

        "risk_factors":
            risk_factors
    }


# ============================================================
# 7. NEW CULTIVATION RECOMMENDATIONS
# ============================================================

def generate_new_recommendations(
    prediction,
    climate,
    irrigation,
    drought,
    nutrient,
    stress
):

    recommendations = []

    # Suitability
    if prediction["suitability"] == "Suitable":

        recommendations.append(
            "The analysed environmental and soil "
            "conditions are suitable for mango cultivation."
        )

    else:

        recommendations.append(
            "The analysed conditions require attention "
            "before establishing mango cultivation."
        )

    # Climate
    if climate["overall_climate_status"] != "Suitable":

        recommendations.append(
            "Review the identified climate or soil "
            "limitations before cultivation."
        )

    # Irrigation
    if irrigation["level"] in [
        "Moderate",
        "High"
    ]:

        recommendations.append(
            "Prepare supplementary irrigation facilities "
            "for periods of insufficient rainfall."
        )

    # Drought
    if drought["alert"]:

        recommendations.append(
            "Maintain adequate water resources because "
            "drought risk requires attention."
        )

    # Nutrient
    if nutrient["status"] == "Deficient":

        recommendations.append(
            "Conduct soil testing and develop an "
            "appropriate nutrient management plan."
        )

    # Stress
    if stress["level"] in [
        "Moderate",
        "High"
    ]:

        recommendations.append(
            "Monitor environmental stress conditions "
            "during cultivation planning."
        )

    return recommendations


# ============================================================
# 8. EXISTING CULTIVATION RECOMMENDATIONS
# ============================================================

def generate_existing_recommendations(
    prediction,
    irrigation,
    drought,
    nutrient,
    stress,
    disease
):

    recommendations = []

    # --------------------------------------------------------
    # Irrigation
    # --------------------------------------------------------

    if irrigation["level"] == "High":

        recommendations.append(
            "Increase irrigation preparedness and "
            "closely monitor soil moisture."
        )

    elif irrigation["level"] == "Moderate":

        recommendations.append(
            "Monitor soil moisture and provide "
            "supplementary irrigation when required."
        )

    # --------------------------------------------------------
    # Drought
    # --------------------------------------------------------

    if drought["alert"]:

        recommendations.append(
            "Monitor water availability and drought "
            "conditions closely."
        )

    # --------------------------------------------------------
    # Nutrients
    # --------------------------------------------------------

    if nutrient["status"] == "Deficient":

        recommendations.append(
            "Conduct soil testing and review the "
            "nutrient management plan."
        )

    # --------------------------------------------------------
    # Environmental stress
    # --------------------------------------------------------

    if stress["level"] != "Low":

        recommendations.append(
            "Monitor plants for environmental stress "
            "under the current conditions."
        )

    # --------------------------------------------------------
    # Disease risk
    # --------------------------------------------------------

    if disease["risk_level"] in [
        "Moderate",
        "High"
    ]:

        recommendations.append(
            "Increase field monitoring because "
            "environmental conditions may favour "
            "disease development."
        )

    if not recommendations:

        recommendations.append(
            "Current environmental conditions do not "
            "indicate a major advisory concern. "
            "Continue regular crop monitoring."
        )

    return recommendations


# ============================================================
# 9. MAIN ADVISORY FUNCTION
# ============================================================

def generate_advisory(
    mode,
    prediction,
    input_data
):

    # --------------------------------------------------------
    # Common analysis
    # --------------------------------------------------------

    climate = analyze_climate(
        input_data
    )

    irrigation = generate_irrigation_advisory(
        prediction,
        input_data
    )

    drought = generate_drought_advisory(
        prediction,
        input_data
    )

    nutrient = generate_nutrient_advisory(
        prediction,
        input_data
    )

    stress = analyze_environmental_stress(
        prediction,
        input_data
    )

    # ========================================================
    # NEWLY CULTIVATING
    # ========================================================

    if mode == "new":

        recommendations = generate_new_recommendations(
            prediction,
            climate,
            irrigation,
            drought,
            nutrient,
            stress
        )

        return {

            "module":
                "Newly Cultivating Mango Plants",

            "cultivation_suitability": {

                "prediction":
                    prediction["suitability"],

                "status":
                    prediction["suitability"]
            },

            "climate_analysis":
                climate,

            "soil_condition":
                nutrient,

            "nutrient_condition":
               nutrient,    

            "irrigation_preparation":
                irrigation,

            "drought_alert":
                drought,

            "environmental_stress":
                stress,

            "recommended_cultivation_period":
                {
                    "status":
                        "Historical weather analysis required",

                    "message":
                        "Recommended cultivation periods "
                        "will be calculated from the "
                        "historical monthly weather dataset."
                },

            "recommendations":
                recommendations
        }

    # ========================================================
    # CURRENTLY GROWING
    # ========================================================

    elif mode == "existing":

        disease = generate_disease_risk_advisory(
            input_data
        )

        recommendations = generate_existing_recommendations(
            prediction,
            irrigation,
            drought,
            nutrient,
            stress,
            disease
        )

        return {

            "module":
                "Currently Growing Mango Plants",

            "cultivation_condition":
                prediction["suitability"],

            "irrigation_advisory":
                irrigation,

            "environmental_stress":
                stress,

            "drought_alert":
                drought,

            "nutrient_advisory":
                nutrient,

            "disease_risk":
                disease,

            "recommendations":
                recommendations
        }

    else:

        raise ValueError(
            "Invalid mode. Use 'new' or 'existing'."
        )


def generate_live_weather_advisory(current_weather):
    temperature = current_weather.get("temperature_c", 0)
    humidity = current_weather.get("humidity", 0)
    rainfall = current_weather.get("rainfall_1h_mm", 0)
    condition = current_weather.get("condition", "")
    description = current_weather.get("description", "")

    # --------------------------------------------------
    # Irrigation advisory
    # --------------------------------------------------

    if rainfall >= 2:
        irrigation = {
            "level": "Low",
            "message": (
                "Current rainfall is relatively high. "
                "Additional irrigation may not be required."
            ),
            "action": (
                "Avoid unnecessary irrigation and monitor "
                "soil moisture."
            ),
        }
    elif rainfall > 0:
        irrigation = {
            "level": "Monitor",
            "message": "Light rainfall is currently occurring.",
            "action": (
                "Check soil moisture before applying "
                "additional irrigation."
            ),
        }
    elif temperature >= 32:
        irrigation = {
            "level": "Attention",
            "message": (
                "No current rainfall is detected and "
                "temperature is relatively high."
            ),
            "action": (
                "Monitor soil moisture and consider "
                "irrigation if the soil is dry."
            ),
        }
    else:
        irrigation = {
            "level": "Normal",
            "message": (
                "Current weather does not indicate an "
                "immediate irrigation concern."
            ),
            "action": "Continue normal soil-moisture monitoring.",
        }

    # --------------------------------------------------
    # Disease-favouring environment
    # --------------------------------------------------

    disease_factors = []

    if humidity >= 80:
        disease_factors.append("High humidity")

    if rainfall > 0:
        disease_factors.append("Current rainfall")

    if humidity >= 70 and rainfall > 0:
        disease_level = "Moderate"
        disease_message = (
            "Humid and rainy conditions may favour "
            "fungal disease development."
        )
        disease_action = (
            "Inspect mango leaves and fruits regularly "
            "for visible disease symptoms."
        )
    elif humidity >= 85:
        disease_level = "Moderate"
        disease_message = (
            "High humidity may create conditions that "
            "support disease development."
        )
        disease_action = (
            "Increase plant monitoring and maintain "
            "good field ventilation."
        )
    else:
        disease_level = "Low"
        disease_message = (
            "Current weather conditions do not indicate "
            "a strong immediate environmental disease risk."
        )
        disease_action = "Continue normal disease monitoring."

    # --------------------------------------------------
    # Heat stress
    # --------------------------------------------------

    if temperature >= 35:
        heat_stress = {
            "level": "High",
            "message": (
                "Current temperature is very high and "
                "may cause plant heat stress."
            ),
            "action": (
                "Monitor water stress carefully and ensure "
                "adequate moisture availability."
            ),
        }
    elif temperature >= 32:
        heat_stress = {
            "level": "Moderate",
            "message": "Current temperature is relatively high.",
            "action": (
                "Monitor plants for signs of heat "
                "and water stress."
            ),
        }
    else:
        heat_stress = {
            "level": "Low",
            "message": (
                "Current temperature does not indicate "
                "significant heat stress."
            ),
            "action": "Continue normal plant monitoring.",
        }

    # --------------------------------------------------
    # Return live-weather advisory
    # --------------------------------------------------

    return {
        "weather_summary": {
            "temperature_c": temperature,
            "humidity": humidity,
            "rainfall_1h_mm": rainfall,
            "condition": condition,
            "description": description,
        },
        "irrigation": irrigation,
        "disease_environment": {
            "level": disease_level,
            "risk_factors": disease_factors,
            "message": disease_message,
            "action": disease_action,
        },
        "heat_stress": heat_stress,
    }