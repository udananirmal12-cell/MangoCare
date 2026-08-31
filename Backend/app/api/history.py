from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.auth.dependencies import (
    get_current_user
)

from app.database.database import (
    get_db
)

from app.database.db_models import (
    User,
    LeafPrediction,
    FruitPrediction,
    AdvisoryResult
)


router = APIRouter(
    prefix="/api/history",
    tags=["History"]
)


@router.get("")
def get_history(
    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )
):

    leaf_records = (
        db.query(LeafPrediction)
        .filter(
            LeafPrediction.user_id
            == current_user.id
        )
        .order_by(
            LeafPrediction.created_at.desc()
        )
        .all()
    )


    fruit_records = (
        db.query(FruitPrediction)
        .filter(
            FruitPrediction.user_id
            == current_user.id
        )
        .order_by(
            FruitPrediction.created_at.desc()
        )
        .all()
    )


    advisory_records = (
        db.query(AdvisoryResult)
        .filter(
            AdvisoryResult.user_id
            == current_user.id
        )
        .order_by(
            AdvisoryResult.created_at.desc()
        )
        .all()
    )


    history = []


    for item in leaf_records:

        history.append({
            "id": item.id,
            "type": "leaf",
            "title": "Leaf Disease Detection",
            "prediction": item.predicted_class,
            "confidence": item.confidence,
            "image_path": item.image_path,
            "created_at": item.created_at
        })


    for item in fruit_records:

        history.append({
            "id": item.id,
            "type": "fruit",
            "title": "Fruit Condition Detection",
            "prediction": item.predicted_class,
            "confidence": item.confidence,
            "image_path": item.image_path,
            "created_at": item.created_at
        })


    for item in advisory_records:

        history.append({
            "id": item.id,
            "type": "advisory",
            "title": (
                "New Cultivation Advisory"
                if item.mode == "new"
                else "Existing Plant Advisory"
            ),
            "mode": item.mode,
            "suitability": item.suitability,
            "irrigation_need": item.irrigation_need,
            "drought_risk": item.drought_risk,
            "nutrient_condition": item.nutrient_condition,
            "created_at": item.created_at
        })


    history.sort(
        key=lambda x: x["created_at"],
        reverse=True
    )


    return {
        "success": True,
        "total": len(history),
        "history": history
    }