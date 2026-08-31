from fastapi import (
    APIRouter,
    Depends
)

from pydantic import (
    BaseModel,
    Field
)

from sqlalchemy.orm import Session

from app.database.database import (
    get_db
)

from app.database.db_models import (
    User
)

from app.auth.dependencies import (
    get_current_user
)


router = APIRouter(
    prefix="/api/profile",
    tags=["Farmer Profile"]
)


# ==================================================
# Update request
# ==================================================

class ProfileUpdateRequest(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    district: str | None = None

    soil_ph: float | None = Field(
        default=None,
        ge=3.5,
        le=9.0
    )

    nitrogen: float | None = Field(
        default=None,
        ge=0,
        le=200
    )

    phosphorus: float | None = Field(
        default=None,
        ge=0,
        le=200
    )

    potassium: float | None = Field(
        default=None,
        ge=0,
        le=200
    )


# ==================================================
# Get profile
# ==================================================

@router.get("")
def get_profile(
    current_user: User
        = Depends(get_current_user)
):

    return {

        "id":
            current_user.id,

        "name":
            current_user.name,

        "email":
            current_user.email,

        "district":
            current_user.district,

        "soil_ph":
            current_user.soil_ph,

        "nitrogen":
            current_user.nitrogen,

        "phosphorus":
            current_user.phosphorus,

        "potassium":
            current_user.potassium,

        "created_at":
            current_user.created_at
    }


# ==================================================
# Update profile
# ==================================================

@router.put("")
def update_profile(
    request: ProfileUpdateRequest,

    current_user: User
        = Depends(get_current_user),

    db: Session
        = Depends(get_db)
):

    update_data = (
        request.model_dump(
            exclude_unset=True
        )
    )


    for field, value in update_data.items():

        setattr(
            current_user,
            field,
            value
        )


    db.commit()

    db.refresh(
        current_user
    )


    return {

        "success": True,

        "message":
            "Profile updated successfully.",

        "profile": {

            "id":
                current_user.id,

            "name":
                current_user.name,

            "email":
                current_user.email,

            "district":
                current_user.district,

            "soil_ph":
                current_user.soil_ph,

            "nitrogen":
                current_user.nitrogen,

            "phosphorus":
                current_user.phosphorus,

            "potassium":
                current_user.potassium
        }
    }