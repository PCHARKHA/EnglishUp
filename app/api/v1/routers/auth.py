from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token, hash_password
from app.db.session import get_db
from app.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# -------------------------
# Response schema for register
# -------------------------
class RegisterResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


# -------------------------
# LOGIN
# -------------------------
@router.post("/login", response_model=TokenResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == login_data.email.lower()
    ).first()

    if not user or not verify_password(
        login_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# -------------------------
# REGISTER
# -------------------------
@router.post("/register", response_model=RegisterResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    email = user_data.email.lower()

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        name=user_data.name,
        email=email,
        hashed_password=hashed_pw,
        age=user_data.age,
        job_role=user_data.job_role,
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise

    access_token = create_access_token(
        data={"sub": str(new_user.id)}
    )

    return {
        "user": new_user,
        "access_token": access_token,
        "token_type": "bearer",
    }
