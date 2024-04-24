from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from modelling import process_features, make_prediction
from models import User
from db_operations import (create_user,
                           get_user_by_email,
                           get_users,
                           create_or_update_user_session, delete_user)

from config import Config
from serializers import user_serializer

app = Flask(__name__)


@app.route("/account/login/", methods=["POST"])
def login():
    email = request.form.to_dict().get("email", None)
    password = request.form.to_dict().get("password", None)

    if email is None or password is None:
        return jsonify({"message": "Missing email or password", "code": 400}), 400
    else:
        result = get_user_by_email(email)
        if result[1]:
            user = result[0]
            password = check_password_hash(user.get_password(), password)
            if password is not None:
                session = create_or_update_user_session(email, 1)
                if session[1]:
                    return jsonify({"message": "Login successfully!", "code": 200}), 200
                else:
                    return jsonify({"message": session[0], "code": 401}), 401
        return jsonify({"message": "Invalid email or password", "code": 401}), 401


@app.route("/account/logout/", methods=["GET"])
def logout():
    email = request.args.get("email", None)
    session = create_or_update_user_session(email, 0)
    if session[1]:
        return jsonify({"message": "Logged out successfully!", "code": 200}), 200
    else:
        return jsonify({"message": session[0], "code": 401}), 401


@app.route("/users/", methods=["POST", "GET"])
def users_view():
    if request.method == "POST":
        name = request.form.to_dict().get("name", None)
        email = request.form.to_dict().get("email", None)
        password = request.form.to_dict().get("password", None)

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)

        result = create_user(user)

        if result[1]:
            return jsonify({
                "name": user.get_name(),
                "email": user.get_email(),
                "code": 201
            }), 201
        else:
            return {"message": result[0]}, 400

    elif request.method == "GET":
        result = get_users()
        if result[1]:
            return jsonify(user_serializer(result[0], True)), 200
        else:
            return jsonify({"message": result[0], "code": 500}), 500


@app.route("/users/<user_email>/", methods=["GET", "DELETE"])
def user_detail(user_email):
    if request.method == "GET":
        result = get_user_by_email(user_email)
        if result[1]:
            return jsonify(user_serializer(result[0], False)), 200
        else:
            return jsonify({"message": result[0], "code": 400}), 400
    elif request.method == "DELETE":
        result = get_user_by_email(user_email)
        code = 400
        if result[1]:
            result = delete_user(user_email)
            if result[1]:
                code = 204
        return jsonify({"message": result[0], "code": code}), code


@app.route("/model/predict/", methods=["POST"])
def get_model_prediction():
    if len(request.form.to_dict().keys()) == 0:
        data = request.json
    else:
        data = request.form.to_dict()
    nighttime_phone_usage_per_day = data.get("nighttime_phone_usage_per_day", None)
    step_count = data.get("step_count", None)
    in_bed_awake_duration = data.get("in_bed_awake_duration", None)
    actual_sleep_duration = data.get("actual_sleep_duration", None)
    total_phone_usage_per_day = data.get("total_phone_usage_per_day", None)
    calories_burnt = data.get("calories_burnt", None)
    phone_unlock_count_per_day = data.get("phone_unlock_count_per_day", None)
    features = (nighttime_phone_usage_per_day, step_count,
                in_bed_awake_duration, actual_sleep_duration,
                total_phone_usage_per_day, calories_burnt,
                phone_unlock_count_per_day)
    if None not in features:
        features = [float(feature) for feature in features]
        features_ = process_features(features)
        pred = make_prediction(features_)
        predictors = {
            "nighttime_phone_usage_per_day": ("night time phone usage / day (minutes)", features[0]),
            "step_count": ("step count", features[1]),
            "in_bed_awake_duration": ("in bed awake duration (minutes)", features[2]),
            "actual_sleep_duration": ("actual sleep duration (minutes)", features[3]),
            "total_phone_usage_per_day": ("total phone usage / day (minutes)", features[4]),
            "calories_burnt": ("calories burnt (kcal)", features[5]),
            "phone_unlock_count_per_day": ("phone unlock count / day", features[6])
        }

        return jsonify({"message": "Successful",
                        "code": 200,
                        "prediction": pred,
                        "predictors": predictors})
    else:
        return jsonify({"message": "You did not provide all features", "code": 400}), 400


@app.route("/model/recommendation/")
def get_recommendation():
    # TODO document why this method is empty
    pass


if __name__ == "__main__":
    app.run(host=Config.host, port=Config.port)
