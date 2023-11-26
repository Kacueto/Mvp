class Restaurante:
    def __init__(self, data):
        self.restaurante_id = data["RestauranteId"]
        self.direccion = data["Direccion"]
        self.telefono = data["Telefono"]
        self.cantidad_mesas = data["CantidadDeMesas"]
