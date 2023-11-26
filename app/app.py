from flask import Flask, g, request, jsonify
from common.dbConnection import db_connection
from flask_cors import CORS
import hashlib
from model.usuario import Usuario
from model.cliente import Cliente
from model.restaurante import Restaurante

app = Flask(__name__)

CORS(app, origins="http://127.0.0.1:5500")


# Ruta para agregar un nuevo usuario
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    try:
       
        usuario = Usuario(request.json)
    except Exception as e:
        
        return jsonify({'error': 'Error al procesar los parámetros'}), 400
    
    if usuario.nombre is None or usuario.contrasena is None:
        return jsonify({'error': 'Nombre de usuario y contraseña son obligatorios'}), 400

    try:
       
        cursor = db_connection.cursor()

        # Verificar si el usuario ya existe
        
        cursor.execute("SELECT UsuarioID FROM Usuarios WHERE NombreUsuario = %s", (usuario.nombre,))
        usuario_existente = cursor.fetchone()
        
        #agregar verificacion si existe el restaurante con elr estaurante id.
        
        if usuario_existente:
            
            return jsonify({'error': 'El usuario ya existe'}), 409  

        # Aplicar hash a la contraseña antes de almacenarla
        hashed_contrasena = hashlib.sha256(usuario.contrasena.encode('utf-8')).hexdigest()

        # Insertar nuevo usuario en la tabla Usuarios
        cursor.execute("INSERT INTO Usuarios (NombreUsuario, Contraseña) VALUES (%s, %s)", (usuario.nombre, hashed_contrasena))
        db_connection.commit()

        #buscar Idusuario del usuario insertado justo anteriormente
        cursor.execute("SELECT MAX(UsuarioID) FROM Usuarios")
        ultimo_id = cursor.fetchone()[0]
        

        if usuario.tipo_usuario == "Cliente":
            resultado_agregar_cliente = agregar_cliente(usuario.datos_cliente, ultimo_id)
            if 'error' in resultado_agregar_cliente:
                # Manejar el error si ocurrió al agregar el cliente
                return jsonify(resultado_agregar_cliente), 500
        else:
            cursor.execute("SELECT RestauranteID FROM Restaurantes WHERE RestauranteID= %s",(usuario.datos_restaurante.restaurante_id,))
            restaurante_existente = cursor.fetchone()
            if restaurante_existente:
                return jsonify({'error': 'El restaurante ya existe'}), 409 
            resultado_agregar_restaurante = agregar_restaurante(usuario.datos_restaurante, ultimo_id)
            if 'error' in resultado_agregar_restaurante:
                # Manejar el error si ocurrió al agregar el restaurante
                return jsonify(resultado_agregar_restaurante), 500
            
        
        
        return jsonify({'mensaje': 'Usuario agregado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()



def agregar_cliente( cliente, usuario_id):
    
    try:
        
        cursor = db_connection.cursor()

        # Insertar nuevo cliente en la tabla Clientes asociado al usuario_id
        cursor.execute("INSERT INTO Clientes (Nombre, Apellido, CorreoElectronico, Teléfono, UsuarioID) VALUES (%s, %s, %s, %s, %s)", (cliente.nombre, cliente.apellido, cliente.correo, cliente.telefono, usuario_id))
        db_connection.commit()

        return {'mensaje': 'Cliente agregado correctamente'}
    except Exception as e:
        # Manejo de errores específico para agregar_cliente
        return {'error': str(e)}
    finally:
        cursor.close()

def agregar_restaurante(restaurante, usuario_id):
    
    try:
        
        cursor = db_connection.cursor()

        # Insertar nuevo restaurante en la tabla Restaurantes asociado al usuario_id
        cursor.execute("INSERT INTO Restaurantes (RestauranteID, Dirección, Teléfono, CantidadMesas, UsuarioID) VALUES (%s, %s, %s, %s, %s)", ( restaurante.restaurante_id, restaurante.direccion, restaurante.telefono, restaurante.cantidad_mesas, usuario_id))
        db_connection.commit()
        
        for i in range(restaurante.cantidad_mesas):
            
            agregar_mesas(restaurante.restaurante_id)

        return {'mensaje': 'Restaurante agregado correctamente'}
    except Exception as e:
        # Manejo de errores específico para agregar_restaurante
        return {'error': str(e)}
    finally:
        cursor.close()

@app.route('/verificar_login', methods=['POST'])
def verificar_login():
    login = Usuario(request.json)
    print(login.contrasena)

    if login.nombre is None or login.contrasena is None:
        return jsonify({'error': 'Nombre de usuario y contraseña son obligatorios'}), 400

    try:
        
        cursor = db_connection.cursor()

        # Buscar el usuario por nombre de usuario
        cursor.execute("SELECT * FROM Usuarios WHERE NombreUsuario = %s", (login.nombre,))
        usuario = cursor.fetchone()
        if usuario is None or not verificar_contraseña(login.contrasena, usuario[2]):
            return jsonify({'error': 'Nombre de usuario o contraseña incorrectos'}), 401
        
        # Puedes devolver información adicional sobre el usuario si es necesario
        return jsonify({'mensaje': 'Inicio de sesión exitoso', 'UsuarioID': usuario[0], 'NombreUsuario': usuario[1]}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()

import hashlib

def verificar_contraseña(contraseña_ingresada, contraseña_almacenada):
    # Calcula el hash SHA-256 de la contraseña proporcionada durante el inicio de sesión
    hash_ingresado = hashlib.sha256(contraseña_ingresada.encode('utf-8')).hexdigest()

    # Compara el hash calculado con el hash almacenado
    return hash_ingresado == contraseña_almacenada

def agregar_mesas(RestauranteID):
    try:
        
        cursor = db_connection.cursor()
        
        # Buscar el usuario por nombre de usuario
        cursor.execute("INSERT INTO Mesas (RestauranteID, Disponibilidad) VALUES (%s, %s)", (RestauranteID, 0 ))
        db_connection.commit()
        

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()

@app.route('/obtener_mesas_por_restaurante', methods=['POST'])
def obtener_mesas_por_restaurante():
    datos_request = request.json
    restaurante_id = datos_request.get('restaurante_id')

    if restaurante_id is None:
        return jsonify({'error': 'RestauranteID es obligatorio'}), 400

    try:
        cursor = db_connection.cursor()

        # Obtener todas las mesas del restaurante
        cursor.execute("SELECT * FROM Mesas WHERE RestauranteID = %s", (restaurante_id,))
        mesas = cursor.fetchall()

        return jsonify({'mesas': mesas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

        
if __name__ == '__main__':
    app.run(debug=True)
