from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from sqlalchemy.orm import Session

from app.database.database import (
    get_db
)

from app.database.db_models import (
    User
)

from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.auth.dependencies import (
    get_current_user
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# ==================================================
# Schemas
# ==================================================

class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100
    )



class LoginRequest(BaseModel):

    email: EmailStr
    password: str


# ==================================================
# Register
# ==================================================

@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )


    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists."
        )


    user = User(

        name=request.name,

        email=request.email,

        password_hash=hash_password(
            request.password
        )
    )


    db.add(user)
    db.commit()
    db.refresh(user)


    token = create_access_token(
        user.id
    )


    return {

        "success": True,

        "message":
            "Account created successfully.",

        "access_token":
            token,

        "token_type":
            "bearer",

        "user": {

            "id":
                user.id,

            "name":
                user.name,

            "email":
                user.email,

        }
    }


# ==================================================
# Login
# ==================================================

@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.email == request.email
        )
        .first()
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    if not verify_password(
        request.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    token = create_access_token(
        user.id
    )


    return {

        "success": True,

        "access_token":
            token,

        "token_type":
            "bearer",

        "user": {

            "id":
                user.id,

            "name":
                user.name,

            "email":
                user.email,

            "district":
                user.district
        }
    }


# ==================================================
# Current user
# ==================================================

@router.get("/me")
def get_me(
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