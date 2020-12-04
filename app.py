import datetime
import json
from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Roles, Account, DjProfile
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from os import access, environ
import config


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(config.Base)
db.init_app(app)
jwt = JWTManager(app)
Migrate(app, db)
CORS(app)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


@app.route('/')
def main():
    return render_template('index.html')


## Crear y borrar Cuenta, en la tabla de roles en su workbench generar 3 tipos de cuenta
## Id queda vacío, nombre (una cliente, otra dj, otra admin), en status insertar un 1
@app.route('/user/register', methods=['POST', 'DELETE'])
def register():
    if request.method == 'POST':
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        email = request.json.get("email", None)
        role = request.json.get("role", None)

        if not username:
            return jsonify({"msg": "Se requiere nombre de usuario"}), 400
        if not password:
            return jsonify({"msg": "Se requiere una contraseña"}), 400
        if not email:
            return jsonify({"msg": "Se requiere un correo electronico"}), 400

        user = Account.query.filter_by(username=username).first()
        if user:
            return jsonify({"msg": "Nombre de usuario ya existe"}), 400

        user_email = Account.query.filter_by(email=email).first()
        if user_email:
            return jsonify({"msg": "Correo electronico ya existe"}), 400

        account = Account()
        account.username = username
        account.email = email
        account.password = generate_password_hash(password)
        account.role_id = role
        account.save()
        return jsonify(account.serialize()), 201

    if request.method == 'DELETE':
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username:
            return jsonify({"msg": "Nombre de usuario es requerido"}), 400
        if not password:
            return jsonify({"msg": "Password es requerido"}), 400

        account = Account.query.filter_by(username=username).first()
        if account:
            if check_password_hash(account.password, password):
                account.delete()
                return jsonify({"msg": "Cuenta ha sido borrada exitosamente"})
            else:
                return jsonify({"msg": "Clave no coincide con usuario"})
        else:
           return jsonify({"msg": "No existe tal cuenta"}) 

#login usuario
@app.route('/user/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        if not username:
            return jsonify({"msg": "Se requiere un nombre de usuario"}), 400
        if not password:
            return jsonify({"msg": "Se requiere una contraseña"}), 400      
    
        account = Account.query.filter_by(username=username).first()
        if not account:
                return jsonify({"msg": "Clave o usuario incorrecto"}), 401

        if not check_password_hash(account.password, password):
                return jsonify({"msg": "Clave o usuario incorrecto"}), 401

        expires = datetime.timedelta(days=3)
        access_token = create_access_token(identity=account.username, expires_delta=expires)
        data = {
            "token_de_acceso": access_token,
            "cuenta": account.serialize(),
            "expira_en": expires.total_seconds()*1000

        }

        return jsonify(data), 200

## crear Perfl DJ (falta backref a account? borrar account = borrar perfil)
@app.route('/profile/dj', methods=['POST', 'DELETE'])
@jwt_required
def profile():
    if request.method == 'POST':
        username = get_jwt_identity()
        account = Account.query.filter_by(username=username).first()
        djprofile = DjProfile.query.filter_by(dj_id=account.role_id).first()
        if djprofile:
            return jsonify({"msg": "Usuario ya tiene un perfil"})
        if account.role_id != 2:
            return jsonify({"msg": "usuario no es un DJ"})
        else:
            artista = request.json.get("artista", None)
            ciudad = request.json.get("ciudad", None)
            pais = request.json.get("pais", None)
            mixcloud = request.json.get("mixcloud")
            soundcloud = request.json.get("soundcloud")
            spotify = request.json.get("spotify")
            generos = request.json.get("generos", None)
            servicios = request.json.get("servicios", None)
            tecnica = request.json.get("tecnica", None)
            agregar_cancion = request.json.get("agregar_cancion")
            url_cancion = request.json.get("url_cancion")
            biografia = request.json.get("artista")
            dur_min = request.json.get("dur_min")
            dur_max = request.json.get("dur_max")
            staff = request.json.get("staff")
            arrienda_equipos = request.json.get("arrienda_equipos")
            requisitos = request.json.get("requisitos")
            datos = request.json.get("datos")
            

            if not artista:
                return jsonify({"msg": "Se requiere nombre de artista"}), 400
            if not ciudad:
                return jsonify({"msg": "Se requiere que incluyas una ciudad de origen"}), 400
            if not pais:
                return jsonify({"msg": "Se requiere que incluyas un pais de origen"}), 400
            if not servicios:
                return jsonify({"msg": "Se requiere que incluyas como minimo un genero"}), 400
            if not servicios:
                return jsonify({"msg": "Se requiere que incluyas como minimo un servicio"}), 400
            if not tecnica:
                return jsonify({"msg": "Se requiere que especifiques una técnica"}), 400

            dj = DjProfile()
            dj.dj_id = account.id
            dj.artista = artista
            dj.ciudad = ciudad
            dj.pais = pais
            dj.mixcloud = mixcloud
            dj.soundcloud = soundcloud
            dj.spotify = spotify
            dj.generos = json.dumps(generos)
            dj.servicios = json.dumps(servicios)
            dj.tecnica = json.dumps(tecnica)
            dj.agregar_cancion = agregar_cancion
            dj.url_cancion = url_cancion
            dj.biografia = biografia
            dj.dur_min = dur_max
            dj.dur_max = dur_max
            dj.staff = staff
            dj.arrienda_equipos = arrienda_equipos
            dj.requisitos = requisitos
            dj.datos = datos
            dj.save()
            return jsonify(dj.serialize()), 201

if __name__ == '__main__':
    manager.run()
