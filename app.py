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
    nombre_usuario = datos_usuario.get('nombre_usuario')
    contrasena = datos_usuario.get('contrasena')

    if nombre_usuario is None or contrasena is None:
        return jsonify({'error': 'Nombre de usuario y contraseña son obligatorios'}), 400

    try:
        db = get_db()
        cursor = db.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT UsuarioID FROM Usuarios WHERE NombreUsuario = %s", (nombre_usuario,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            return jsonify({'error': 'El usuario ya existe'}), 409  # Código de estado 409 para conflicto

        # Aplicar hash a la contraseña antes de almacenarla
        hashed_contrasena = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

        # Insertar nuevo usuario en la tabla Usuarios
        cursor.execute("INSERT INTO Usuarios (NombreUsuario, Contraseña) VALUES (%s, %s)", (nombre_usuario, hashed_contrasena))
        db.commit()

        return jsonify({'mensaje': 'Usuario agregado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
if __name__ == '__main__':
    app.run(debug=True)
