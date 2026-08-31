import os
import json
import joblib

from datetime import datetime

from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.models.model_predictor import predict_advisory
from app.models.advisory_engine import (
    generate_advisory,
    generate_live_weather_advisory
)


from app.services.weather_service import (
    get_historical_weather_features,
    get_current_weather
)

from app.database.database import get_db
from app.database.db_models import AdvisoryResult
from app.auth.dependencies import get_current_user
from app.database.db_models import User


router = APIRouter(
    prefix="/api/advisory",
    tags=["Smart Advisory"]
)


# --------------------------------------------------
# Load trained advisory package
# --------------------------------------------------

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.abspath(
    os.path.join(
        CURRENT_DIR,
        "..",
        "models",
        "mango_advisory_model.pkl"
    )
)

package = joblib.load(
    MODEL_PATH
)


# --------------------------------------------------
# Request schema
# --------------------------------------------------

class AdvisoryRequest(BaseModel):

    mode: str = Field(
        pattern="^(new|existing)$"
    )

    district: str = Field(
        min_length=2,
        max_length=50
    )

    N: float = Field(
        ge=0,
        le=200
    )

    P: float = Field(
        ge=0,
        le=200
    )

    K: float = Field(
        ge=0,
        le=200
    )

    ph: float = Field(
        ge=3.5,
        le=9.0
    )


# --------------------------------------------------
# Advisory endpoint
# --------------------------------------------------
@router.post("")
def get_advisory(
    request: AdvisoryRequest,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    try:

        # ------------------------------------------
        # Current month
        # ------------------------------------------

        current_month = datetime.now().month


        # ------------------------------------------
        # Historical weather
        # ------------------------------------------

        historical_weather = (
            get_historical_weather_features(
                district=request.district,
                month=current_month
            )
        )


        # ------------------------------------------
        # Build Random Forest input
        # ------------------------------------------

        model_input = {

            "N": request.N,
            "P": request.P,
            "K": request.K,
            "ph": request.ph,

            **historical_weather
        }


        # ------------------------------------------
        # Random Forest Prediction
        # ------------------------------------------

        prediction = predict_advisory(
            model_input,
            package
        )


        # ------------------------------------------
        # Farmer-friendly advisory
        # ------------------------------------------

        advisory = generate_advisory(
            mode=request.mode,
            prediction=prediction,
            input_data=model_input
        )


        # ------------------------------------------
        # Existing plants:
        # Add current/live weather
        # ------------------------------------------

        current_weather = None
        live_weather_advisory = None

        if request.mode == "existing":

            current_weather = get_current_weather(
                request.district
            )

            live_weather_advisory = (
                generate_live_weather_advisory(
                current_weather
                )
            )


        # ------------------------------------------
        # Store complete result
        # ------------------------------------------

        full_advisory_data = {

            "district":
                request.district,

            "historical_weather":
                historical_weather,

            "current_weather":
                current_weather,

            "advisory":
                advisory,

            "live_weather_advisory":
              live_weather_advisory

        }

        database_record = AdvisoryResult(

            user_id=current_user.id,

            mode=request.mode,

            suitability=prediction.get(
                "suitability"
            ),

            irrigation_need=prediction.get(
                "irrigation_need"
            ),

            drought_risk=prediction.get(
                "drought_risk"
            ),

            nutrient_condition=prediction.get(
                "nutrient_condition"
            ),

            advisory_data=json.dumps(
                full_advisory_data
            )
        )


        db.add(
            database_record
        )

        db.commit()

        db.refresh(
            database_record
        )


        # ------------------------------------------
        # API Response
        # ------------------------------------------

        return {

            "success": True,

            "advisory_id":
                database_record.id,

            "mode":
                request.mode,

            "district":
                request.district,

            "prediction":
                prediction,

            "historical_weather":
                historical_weather,

            "current_weather":
                current_weather,

            "advisory":
                advisory,

            "live_weather_advisory":
              live_weather_advisory    
        }


    except ValueError as error:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


    except Exception as error:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )