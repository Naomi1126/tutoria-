from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import Base, engine, SessionLocal
import models

from fastapi.security import OAuth2PasswordBearer
from security import decode_token
from models import User

# Creamos la app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Hola, este es mi backend con FastAPI "}

# Otra ruta de ejemplo
@app.get("/saludo/{nombre}")
def read_item(nombre: str):
    return {"mensaje": f"Hola {nombre}, bienvenido a Mi TutorIA "}



# Dependencia: obtener sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    data = db.query(User).all()
    return [{"id": u.id, "email": u.email, "full_name": u.full_name} for u in data]


# ----------- ENDPOINT DE PRUEBA DE BASE DE DATOS -----------
@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    # SELECT 1 para comprobar conexión
    result = db.execute(text("SELECT 1")).scalar()
    ok = (result == 1)
    return {"status": "ok" if ok else "fail", "db": "connected" if ok else "error"}
# ------------------------------------------------------------

# ----------- Obtener el ususario -----------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    data = decode_token(token)
    if not data or "sub" not in data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    email = data["sub"]
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user

from schemas import UserRead

@app.get("/auth/me", response_model=UserRead)
def read_me(current_user = Depends(get_current_user)):
    return current_user

# routers 
from routers import auth
app.include_router(auth.router)