import logging
from flask import Blueprint, jsonify, render_template, request, send_file
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from app.models import User
from app.schemas import UserSchema, LoginSchema


main = Blueprint("main", __name__)
jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})


user_schema = UserSchema()
login_schema = LoginSchema()


@main.route("/")
def home():
    """ Home function """
    return send_file('../static/index.html'), 200


@main.route("/register", methods=["POST"])
def create_user():
    """Recibe parámetros a través de la consulta y crea el usuario."""
    try:
        args_json = request.get_json()
        try:
            args = user_schema.load(args_json)
        except Exception as e:
            print(e)
            raise e
        else:
            email = args["email"]
            password = args["password"]
            user_exists = User.exists(email)

            if user_exists:
                return jsonify("Usuario ya existe"), 400

            user = User(**args)
            user.set_password(password)
            user.set_email_lower(email)
            user.save_to_db()
            return jsonify("Usuario creado con éxito!"), 201

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en create_user: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/login", methods=["POST"])
def login_user():
    """Recibe parámetros a través de la consulta y retorna un token"""
    try:
        args_json = request.get_json()
        try:
            args = login_schema.load(args_json)
            print(args)
        except Exception as e:
            print(e)
            raise e
        else:
            email = args["email"]
            password = args["password"]
            user = User.find_by_email(email)

            if user is None or \
               user.check_password(password) == False:
                return jsonify("ERROR DE USUARIO O CONTRASEÑA"), 400

            access_token = create_access_token(email)
            user.is_disabled = False
            user.save_to_db()

            return jsonify(
                    {
                        "token": access_token,
                        "user": user_schema.dump(user),
                        "email": user.email,
                        "username": user.username,
                        "user_id": user.id,
                    }
            ), 200
    except Exception as e:
        error_message = str(e)
        print(e)
        logging.error(f"Error en login_user: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/user/<int:user_id>")
def get_user(user_id):
    """Retorna la información del usuario según su ID"""
    try:
        user = User.find_by_id(user_id)
        if user:
            print(user)
            return jsonify(user_schema.dump(user))

        return jsonify("Usuario no encontrado"), 404

    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en get_user: {error_message}")
        return jsonify("ERROR"), 500


@main.route("/userlist/<int:id>", methods=["PUT", "DELETE"])
@jwt_required()
def update_user(id):
    """Recibe parámetros para actualizar o deshabilitar al usuario"""
    try:
        user = User.find_by_id(id)
        uid = get_jwt_identity()
        print("GET_JWT_IDENTITY(): ", uid)
        if user is None:
            return jsonify("USUARIO NO ENCONTRADO"), 404
        if request.method == "DELETE":
            user.is_disabled = True
            user.save_to_db()
            return jsonify("USUARIO DESHABILITADO"), 204
        user.username = request.json.get("username")
        user.save_to_db()
        return jsonify("USUARIO ACTUALIZADO"), 200
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error en update_user: {error_message}")
        return jsonify("ERROR"), 500
