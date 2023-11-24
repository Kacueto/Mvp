from flask import Flask, g, request, jsonify
import mysql.connector
from flask_cors import CORS
import hashlib

app = Flask(__name__)

CORS(app, origins="http://127.0.0.1:5500")
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_DB'] = 'mvpbbd'
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            host=app.config['MYSQL_HOST'],
            database=app.config['MYSQL_DB']
        )
    return g.db

# Ruta para agregar un nuevo usuario
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    datos_usuario = request.json
    nombre_usuario = datos_usuario.get('Usuario')
    contrasena = datos_usuario.get('Contrasena')
    tipo_usuario = datos_usuario.get('TipoUsuario')

    datos_cliente = datos_usuario.get('DatosCliente', {})
    nombre_cliente = datos_cliente.get('Nombre')
    apellido_cliente = datos_cliente.get('Apellido')
    correo_cliente = datos_cliente.get('Correo')
    telefono_cliente = datos_cliente.get('Telefono')

    datos_restaurante = datos_usuario.get('DatosRestaurante', {})
    restaurante_id = datos_restaurante.get('RestauranteId')
    direccion_restaurante = datos_restaurante.get('Direccion')
    telefono_restaurante = datos_restaurante.get('Telefono')
    cantidad_mesas = datos_restaurante.get('CantidadDeMesas')
    
    if nombre_usuario is None or contrasena is None:
        return jsonify({'error': 'Nombre de usuario y contraseña son obligatorios'}), 400

    try:
        db = get_db()
        cursor = db.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT UsuarioID FROM Usuarios WHERE NombreUsuario = %s", (nombre_usuario,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return jsonify({'error': 'El usuario ya existe'}), 409  

        # Aplicar hash a la contraseña antes de almacenarla
        hashed_contrasena = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

        # Insertar nuevo usuario en la tabla Usuarios
        cursor.execute("INSERT INTO Usuarios (NombreUsuario, Contraseña) VALUES (%s, %s)", (nombre_usuario, hashed_contrasena))
        db.commit()

        #buscar Idusuario del usuario insertado justo anteriormente
        cursor.execute("SELECT MAX(UsuarioID) FROM Usuarios")
        ultimo_id = cursor.fetchone()[0]
        print(ultimo_id)
        

        if tipo_usuario == "Cliente":
            resultado_agregar_cliente = agregar_cliente(nombre_cliente, apellido_cliente,correo_cliente, telefono_cliente, ultimo_id)
            if 'error' in resultado_agregar_cliente:
                # Manejar el error si ocurrió al agregar el cliente
                return jsonify(resultado_agregar_cliente), 500
        else:
            resultado_agregar_restaurante = agregar_restaurante(restaurante_id, direccion_restaurante, telefono_restaurante, cantidad_mesas, ultimo_id)
            if 'error' in resultado_agregar_restaurante:
                # Manejar el error si ocurrió al agregar el restaurante
                return jsonify(resultado_agregar_restaurante), 500
            
        
        
        return jsonify({'mensaje': 'Usuario agregado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()



def agregar_cliente(nombre,apellido, correo, telefono, usuario_id):
    try:
        db = get_db()
        cursor = db.cursor()

        # Insertar nuevo cliente en la tabla Clientes asociado al usuario_id
        cursor.execute("INSERT INTO Clientes (Nombre, Apellido, CorreoElectronico, Teléfono, UsuarioID) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, correo, telefono, usuario_id))
        db.commit()

        return {'mensaje': 'Cliente agregado correctamente'}
    except Exception as e:
        # Manejo de errores específico para agregar_cliente
        return {'error': str(e)}
    finally:
        cursor.close()

def agregar_restaurante(restaurante_id, direccion, telefono, cantidad_mesas, usuario_id):
    try:
        db = get_db()
        cursor = db.cursor()

        # Insertar nuevo restaurante en la tabla Restaurantes asociado al usuario_id
        cursor.execute("INSERT INTO Restaurantes (RestauranteID, Direccion, Telefono, CantidadMesas, UsuarioID) VALUES (%s, %s, %s, %s, %s)", (restaurante_id, direccion, telefono, cantidad_mesas, usuario_id))
        db.commit()

        return {'mensaje': 'Restaurante agregado correctamente'}
    except Exception as e:
        # Manejo de errores específico para agregar_restaurante
        return {'error': str(e)}
    finally:
        cursor.close()

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
if __name__ == '__main__':
    app.run(debug=True)
