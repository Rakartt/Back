from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://ec2-54-87-75-89.compute-1.amazonaws.com"]}})

# Configuración de la base de datos con la dns
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mi_usuario:12345@localhost/registro_usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definir el modelo de la tabla Usuarioo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, nombres, apellidos, fecha_nacimiento, password):
        self.nombres = nombres
        self.apellidos = apellidos
        self.fecha_nacimiento = fecha_nacimiento
        self.password = password

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nuevo_usuario = Usuario(
        nombres=data['nombres'],
        apellidos=data['apellidos'],
        fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d'),
        password=data['password']
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@app.route('/registro', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    resultado = [
        {
            "id": usuario.id,
            "nombres": usuario.nombres,
            "apellidos": usuario.apellidos,
            "fecha_nacimiento": usuario.fecha_nacimiento.strftime('%Y-%m-%d')
        }
        for usuario in usuarios
    ]
    return jsonify(resultado)

@app.route('/usuarios/<int:user_id>', methods=['DELETE'])
def eliminar_usuario(user_id):
    usuario = Usuario.query.get(user_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
