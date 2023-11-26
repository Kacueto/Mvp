from model.restaurante import Restaurante
from model.cliente import Cliente

class Usuario:
    def __init__(self, data):
        self.nombre = data.get("Usuario")
        self.contrasena = data.get("Contrasena")
        self.tipo_usuario = data.get("TipoUsuario")
        self.datos_cliente = self.inicializar_cliente(data.get("DatosCliente"))
        self.datos_restaurante = self.inicializar_restaurante(data.get("DatosRestaurante"))

    def inicializar_cliente(self, data_cliente):
        if data_cliente:
            return Cliente(data_cliente)
        else:
            return None

    def inicializar_restaurante(self, data_restaurante):
        if data_restaurante:
            return Restaurante(data_restaurante)
        else:
            return None