from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route("account/login/", methods=["POST"])
def login():
    # TODO document why this method is empty
    pass

@app.route("account/logout/", methods=["GET"])
def logout():
    # TODO document why this method is empty
    pass

@app.route("/users/", methods=["POST", "GET"])
def users_view():
    # TODO document why this method is empty
    pass

@app.route("/users/<int:user_id>/", methods=["PUT", "GET", "DELETE"])
def user_detail():
    # TODO document why this method is empty
    pass

@app.route("model/predict/")
def get_model_prediction():
    # TODO document why this method is empty
    pass

@app.route("model/recommendation/")
def get_recommendation():
    # TODO document why this method is empty
    pass

