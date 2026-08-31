from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.auth.dependencies import (
    get_current_user
)

from app.database.db_models import (
    User
)

from app.services.weather_service import (
    get_current_weather
)


router = APIRouter(
    prefix="/api/weather",
    tags=["Weather"]
)


@router.get("/current")
def current_weather(
    current_user: User = Depends(
        get_current_user
    )
):

    if not current_user.district:

        raise HTTPException(
            status_code=400,
            detail=(
                "Please add your location "
                "to your profile first."
            )
        )


    weather = get_current_weather(
        current_user.district
    )


    return {
        "success": True,
        "location": current_user.district,
        "weather": weather
    }