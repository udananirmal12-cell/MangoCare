import os
import shutil
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    Depends
)

from sqlalchemy.orm import Session

from app.models.fruit_predictor import predict_fruit
from app.database.database import get_db
from app.database.db_models import FruitPrediction
from app.auth.dependencies import get_current_user
from app.database.db_models import User
from app.services.disease_info_service import (
    get_fruit_disease_info
)


router = APIRouter(
    prefix="/api/fruit",
    tags=["Fruit Disease Detection"]
)


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

UPLOAD_DIR = os.path.join(
    BASE_DIR,
    "uploads",
    "fruits"
)

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg"
}


@router.post("/predict")
async def predict_fruit_disease(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),  
    db: Session = Depends(get_db)
):

    if file.content_type not in ALLOWED_TYPES:

        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG images are supported."
        )

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in [".jpg", ".jpeg", ".png"]:
        extension = ".jpg"

    unique_filename = (
        f"{uuid.uuid4()}{extension}"
    )

    image_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    try:

        # Save image
        with open(
            image_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # AI prediction
        result = predict_fruit(
            image_path
        )

        relative_path = (
            f"uploads/fruits/{unique_filename}"
        )

        disease_information = (
             get_fruit_disease_info(
              result["prediction"]
              )
        )

        # Save prediction
        database_record = FruitPrediction(
            user_id=current_user.id,
            image_path=relative_path,
            original_filename=file.filename,
            predicted_class=result["prediction"],
            confidence=result["confidence"]
        )

        db.add(
            database_record
        )

        db.commit()

        db.refresh(
            database_record
        )

        return {
            "success": True,
            "prediction_id": database_record.id,
            "type": "fruit",
            "image_path": relative_path,
            "original_filename": file.filename,
            "result": result,
            "disease_information": disease_information
        }

    except Exception as error:

        db.rollback()

        if os.path.exists(
            image_path
        ):
            os.remove(
                image_path
            )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )