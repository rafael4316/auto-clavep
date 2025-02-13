from database import session, Usuario

# Crear un nuevo usuario (modifica el nombre y la contraseña si lo deseas)
nuevo_usuario = Usuario(username="admin", password="1234")

# Agregar el usuario a la base de datos
session.add(nuevo_usuario)
session.commit()

print("✅ Usuario creado exitosamente")
