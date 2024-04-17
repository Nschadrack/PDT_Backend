from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from db_operations import (create_user, 
                           get_user_by_email, 
                           get_users, 
                           create_or_update_user_session)

from config import Config


app = Flask(__name__)


@app.route("/account/login/", methods=["POST"])
def login():
    print("Request data: ", request.json)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    if email is None or password is None:
        return jsonify({"message": "Missing email or password"}), 400
    else:
        result = get_user_by_email(email)
        if result[1]:
            user = result[0]
            password = check_password_hash(user.get_password(), password)
            if password is not None:
                session = create_or_update_user_session(email, 1)
                if session[1]:
                    return jsonify({"message": "Login successfully!"}), 200
                else:
                    return jsonify({"message": session[0]}), 401
        return jsonify({"message": "Invalid email or password"}), 401
    


@app.route("/account/logout/", methods=["GET"])
def logout():
    email = request.args("email", None)
    session = create_or_update_user_session(email, 0)
    if session[1]:
        return jsonify({"message": "Logged out successfully!"}), 200
    else:
        return jsonify({"message": session[0]}), 401
    


@app.route("/users/", methods=["POST", "GET"])
def users_view():
    # TODO document why this method is empty
    if  request.method == "POST":
        name = request.json.get("name", None)
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)

        result = create_user(user)

        if result[1]:
            return jsonify({
                "name": user.get_name(),
                "email": user.get_email()
            }), 201
        else:
            return result[0], 500

    elif request.method == "GET":
        result = get_users()
        if result[1]:
            return jsonify(result[0]), 200
        else:
            return jsonify({"message": result[0]}), 500
        

@app.route("/users/<int:user_id>/", methods=["PUT", "GET", "DELETE"])
def user_detail():
    # TODO document why this method is empty
    pass

@app.route("/model/predict/")
def get_model_prediction():
    # TODO document why this method is empty
    pass

@app.route("/model/recommendation/")
def get_recommendation():
    # TODO document why this method is empty
    pass



if __name__ == "__main__":
    app.run(host=Config.host, port=Config.port)