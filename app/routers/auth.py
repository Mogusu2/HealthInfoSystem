from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import engine
from app.models.models import Client
from app.schemas.schemas import Token
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta



router = APIRouter(prefix="/auth", tags=["auth"])



SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_session():
    with Session(engine) as session:
        yield session



def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)



def get_password_hash(password):
    return pwd_context.hash(password)



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)





@router.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    existing = session.exec(select(Client).where(Client.email == form_data.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = Client(
        name=form_data.username,
        age=0,
        contact="N/A",
        email=form_data.username,
        hashed_password=get_password_hash(form_data.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"msg": "Client registered"}



@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(Client).where(Client.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}



def get_current_client(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> Client:
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.exec(select(Client).where(Client.email == email)).first()
    if user is None:
        raise credentials_exception
    return user
