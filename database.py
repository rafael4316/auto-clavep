from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Conectar a SQLite
DATABASE_URL = "sqlite:///autoclaves.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Modelo de Usuarios con contraseña cifrada
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Almacenará la contraseña cifrada

# Modelo de Archivos Subidos
class ArchivoSubido(Base):
    __tablename__ = "archivos_subidos"
    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String, nullable=False)
    archivo_nombre = Column(String, nullable=False)
    fecha_subida = Column(DateTime, default=datetime.datetime.utcnow)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)
