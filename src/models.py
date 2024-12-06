import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime, timezone

Base = declarative_base()

# Tabla usuario
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(250), unique=True, nullable=False)
    correo = Column(String(250), unique=True, nullable=False)
    nombre_completo = Column(String(250))
    contraseña = Column(String(250), nullable=False)
    foto_perfil = Column(String(250))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    bio = Column(String(250))
    publicaciones = relationship("Post", back_populates="usuario")
    comentarios = relationship("Comentario", back_populates="usuario")
    historias = relationship("Historia", back_populates="usuario")
    mensajes_enviados = relationship("Mensaje", foreign_keys="Mensaje.usuario_emisor_id", back_populates="emisor")
    mensajes_recibidos = relationship("Mensaje", foreign_keys="Mensaje.usuario_receptor_id", back_populates="receptor")

# Tabla Post (Publicaciones)
class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    comentario = Column(String(250), nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_publicacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    usuario = relationship("Usuario", back_populates="publicaciones")
    comentarios = relationship("Comentario", back_populates="publicacion")
    me_gustas = relationship("MeGusta", back_populates="publicacion")

# Tabla Comentario
class Comentario(Base):
    __tablename__ = 'comentario'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    publicacion_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    texto = Column(Text, nullable=False)
    fecha_comentario = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    usuario = relationship("Usuario", back_populates="comentarios")
    publicacion = relationship("Post", back_populates="comentarios")

# Tabla MeGusta
class MeGusta(Base):
    __tablename__ = 'megusta'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    publicacion_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    usuario = relationship("Usuario", back_populates="me_gustas")
    publicacion = relationship("Post", back_populates="me_gustas")

# Tabla Seguidores
class Seguidores(Base):
    __tablename__ = 'seguidores'
    id = Column(Integer, primary_key=True)
    seguidor_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    seguido_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    fecha_inicio = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Tabla Historia
class Historia(Base):
    __tablename__ = 'historia'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    contenido = Column(String(250), nullable=False)  # img o video
    fecha_publicacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_expiracion = Column(DateTime, nullable=False)
    usuario = relationship("Usuario", back_populates="historias")

# Tabla Mensaje
class Mensaje(Base):
    __tablename__ = 'mensaje'
    id = Column(Integer, primary_key=True)
    usuario_emisor_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    usuario_receptor_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    emisor = relationship("Usuario", foreign_keys=[usuario_emisor_id], back_populates="mensajes_enviados")
    receptor = relationship("Usuario", foreign_keys=[usuario_receptor_id], back_populates="mensajes_recibidos")

# Método to_dict
def to_dict(self):
    return {}

# Crear diagrama de base de datos
try:
    render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e

