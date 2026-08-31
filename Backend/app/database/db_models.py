from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    Boolean
)

from sqlalchemy.orm import relationship

from app.database.database import Base


# ==================================================
# USERS
# ==================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    district = Column(
        String(100),
        nullable=True
    )

    soil_ph = Column(
        Float,
        nullable=True
    )

    nitrogen = Column(
        Float,
        nullable=True
    )

    phosphorus = Column(
        Float,
        nullable=True
    )

    potassium = Column(
        Float,
        nullable=True
    )

    mango_variety = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    leaf_predictions = relationship(
        "LeafPrediction",
        back_populates="user"
    )

    fruit_predictions = relationship(
        "FruitPrediction",
        back_populates="user"
    )

    advisories = relationship(
        "AdvisoryResult",
        back_populates="user"
    )


# ==================================================
# LEAF PREDICTIONS
# ==================================================

class LeafPrediction(Base):

    __tablename__ = "leaf_predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    image_path = Column(
        String(500),
        nullable=False
    )

    original_filename = Column(
        String(255),
        nullable=True
    )

    predicted_class = Column(
        String(100),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="leaf_predictions"
    )


# ==================================================
# FRUIT PREDICTIONS
# ==================================================

class FruitPrediction(Base):

    __tablename__ = "fruit_predictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    image_path = Column(
        String(500),
        nullable=False
    )

    original_filename = Column(
        String(255),
        nullable=True
    )

    predicted_class = Column(
        String(100),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="fruit_predictions"
    )


# ==================================================
# ADVISORY RESULTS
# ==================================================

class AdvisoryResult(Base):

    __tablename__ = "advisory_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    mode = Column(
        String(20),
        nullable=False
    )

    suitability = Column(
        String(100),
        nullable=True
    )

    irrigation_need = Column(
        String(100),
        nullable=True
    )

    drought_risk = Column(
        String(100),
        nullable=True
    )

    nutrient_condition = Column(
        String(100),
        nullable=True
    )

    advisory_data = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="advisories"
    )


# ==================================================
# WEATHER RECORDS
# ==================================================

class WeatherRecord(Base):

    __tablename__ = "weather_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    district = Column(
        String(100),
        nullable=False
    )

    temperature = Column(
        Float,
        nullable=True
    )

    humidity = Column(
        Float,
        nullable=True
    )

    rainfall = Column(
        Float,
        nullable=True
    )

    weather_condition = Column(
        String(100),
        nullable=True
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ==================================================
# NOTIFICATIONS
# ==================================================

class Notification(Base):

    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    notification_type = Column(
        String(50),
        nullable=True
    )

    is_read = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )