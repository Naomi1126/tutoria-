from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi import text
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Usuario


# Creamos la app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego podemos restringirlo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Hola, este es mi backend con FastAPI 🚀"}

# Otra ruta de ejemplo
@app.get("/saludo/{nombre}")
def read_item(nombre: str):
    return {"mensaje": f"Hola {nombre}, bienvenido a Mi Tutor App 👋"}

from database import engine, Base

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Dependencia: obtener sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/usuarios/")
def crear_usuario(nombre: str, correo: str, db: Session = Depends(get_db)):
    usuario = Usuario(nombre=nombre, correo=correo)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.get("/usuarios/")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()
