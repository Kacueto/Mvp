from flask import Flask, g, request, jsonify
from common.dbConnection import db_connection
from flask_cors import CORS
import hashlib
from model.usuario import Usuario
from model.cliente import Cliente
from model.restaurante import Restaurante
import json
from datetime import datetime, timedelta

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
    

    if login.nombre is None or login.contrasena is None:
        return jsonify({'error': 'Nombre de usuario y contraseña son obligatorios'}), 400

    try:
        
        cursor = db_connection.cursor()

        # Buscar el usuario por nombre de usuario
        cursor.execute("SELECT * FROM Usuarios WHERE NombreUsuario = %s", (login.nombre,))
        usuario = cursor.fetchone()
        if usuario is None or not verificar_contraseña(login.contrasena, usuario[2]):
            return jsonify({'error': 'Nombre de usuario o contraseña incorrectos'}), 401
        print(usuario[0])
        
        
       
        cursor.execute("SELECT * from Restaurantes where UsuarioID = %s",(usuario[0],))
        tipov = cursor.fetchone()
        if tipov is None:
            tipo = 'cliente'
            cursor.execute("SELECT * from clientes where UsuarioID = %s",(usuario[0],))
            tipov = cursor.fetchone()
            tipov = {
                'ClienteID': tipov[0],
                'UsuarioID': tipov[1],
                'Nombre': tipov[2],
                'Apellido': tipov[3],
                'Correo': tipov[4],
                'Telefono': tipov[5]
            }  
        else:   
            tipo = 'restaurante' 
            tipov = {
                'RestauranteID': tipov[0],
                'UsuarioID': tipov[1],
                'Direccion': tipov[2],
                'Telefono': tipov[3]
            }   
        
            
       
        # Puedes devolver información adicional sobre el usuario si es necesario
        return jsonify({'NombreUsuario': usuario[1], 'tipo': tipo, 'infousuario' : tipov}), 200
        
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
        mi_json =[{"MesaID": item[0], "RestauranteID": item[1], "Disponibilidad": item[2]} for item in mesas]
        return jsonify({'mesas': mi_json})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()

@app.route('/hacer_reservacion', methods=['POST'])
def hacer_reservacion():
    datos = request.json
    cliente_id = datos.get('cliente_id')
    restaurante_id = datos.get('restaurante_id')
    mesa_id = datos.get('mesa_id')
    fecha = datos.get('fecha')
    try:
        cursor = db_connection.cursor()

        cursor.execute("INSERT INTO reservaciones (ClienteID, RestauranteID, MesaID, FechaReservacion) values(%s,%s,%s,%s)",(cliente_id, restaurante_id,mesa_id,fecha))
        db_connection.commit()
        return jsonify({'mensaje': 'insercion exitosa'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
@app.route('/estadisticas_restaurante', methods=['GET'])
def estadisticas_restaurante():
    datos = request.json
    restaurante_id = datos.get('restaurante_id')
    try:
        cursor = db_connection.cursor()

        # Obtener el número de clientes en el mes actual
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        fecha_inicio_mes = datetime(año_actual, mes_actual, 1)
        cursor.execute("SELECT COUNT(DISTINCT ClienteID) FROM reservaciones WHERE RestauranteID = %s AND MONTH(FechaReservacion) = %s AND YEAR(FechaReservacion) = %s", (restaurante_id, mes_actual, año_actual))
        clientes_en_mes = cursor.fetchone()[0]

        # Obtener el número de reservas totales en los últimos 3 meses
        fecha_inicio_ultimos_3_meses = datetime.now() - timedelta(days=90)
        cursor.execute("SELECT COUNT(*) FROM reservaciones WHERE RestauranteID = %s AND FechaReservacion >= %s", (restaurante_id, fecha_inicio_ultimos_3_meses))
        reservas_ultimos_3_meses = cursor.fetchone()[0]

        return jsonify({
            'clientes_en_mes': clientes_en_mes,
            'reservas_ultimos_3_meses': reservas_ultimos_3_meses
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
@app.route('/eliminar_reserva/<int:reserva_id>', methods=['DELETE'])
def eliminar_reserva(reserva_id):
    try:
        cursor = db_connection.cursor()

    # Verificar si la reserva existe antes de intentar eliminarla
        cursor.execute("SELECT * FROM reservaciones WHERE ReservacionID = %s", (reserva_id,))
        reserva = cursor.fetchone()
        
        if not reserva:
            return jsonify({'mensaje': 'Reserva no encontrada'}), 404

        # Eliminar la reserva
        cursor.execute("DELETE FROM reservaciones WHERE ReservacionID = %s", (reserva_id,))
        db_connection.commit()

        return jsonify({'mensaje': 'Reserva eliminada correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()    
if __name__ == '__main__':
    app.run(debug=True)
