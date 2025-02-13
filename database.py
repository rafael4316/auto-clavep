from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

DATABASE_URL = "sqlite:///autoclaves.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()

# Modelo para almacenar los registros de autoclaves
class RegistroAutoclave(Base):
    __tablename__ = "registros_autoclave"

    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String, index=True)
    autoclave = Column(Integer)
    fecha_subida = Column(DateTime, default=datetime.datetime.utcnow)

# Modelo para Usuarios (Autenticación)
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)  # Aquí puedes encriptar las contraseñas en el futuro

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)
