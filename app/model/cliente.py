
class Cliente:
    def __init__(self, data):
        self.nombre = data["Nombre"]
        self.apellido = data["Apellido"]
        self.correo = data["Correo"]
        self.telefono = data["Telefono"]
