from database import session, Usuario

# Lista de usuarios predefinidos
usuarios = [
    {"username": "mateo", "password": "sertech12345@@"},
    {"username": "panafoods", "password": "conserva12345@"}
]

for user in usuarios:
    # Verificar si el usuario ya existe
    existe = session.query(Usuario).filter_by(username=user["username"]).first()
    if not existe:
        nuevo_usuario = Usuario(username=user["username"], password=user["password"])
        session.add(nuevo_usuario)

session.commit()
print("Usuarios creados exitosamente (si no existían)")
