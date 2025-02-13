from database import session, Usuario
from werkzeug.security import generate_password_hash

# Lista de usuarios a crear
usuarios = [
    {"username": "mateo", "password": "sertech12345@@"},
    {"username": "panafoods", "password": "conserva12345@"},
]

# Crear y agregar los usuarios a la base de datos
for user in usuarios:
    usuario_existente = session.query(Usuario).filter_by(username=user["username"]).first()
    
    if usuario_existente:
        print(f"⚠️ El usuario '{user['username']}' ya existe. No se creará de nuevo.")
    else:
        nuevo_usuario = Usuario(
            username=user["username"],
            password=generate_password_hash(user["password"])  # Cifrar la contraseña
        )
        session.add(nuevo_usuario)
        print(f"✅ Usuario '{user['username']}' creado exitosamente.")

# Guardar cambios en la base de datos
session.commit()
print("🎉 Todos los usuarios fueron creados correctamente.")
