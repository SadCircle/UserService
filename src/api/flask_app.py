from flask import Flask, request, jsonify
from service.user import UserService
import bootstrap
from view import (
    all_users
)


app = Flask(__name__)
uow = bootstrap.bootstrap()


@app.route("/user/<userid>", methods=["GET"])
def get_user(userid: int):
    user_service = UserService()
    user = user_service.get_user(uow, userid)
    if user:
        return jsonify(user), 200
    else:
        return "NOT FOUND", 404


@app.route("/user/add", methods=["POST"])
def add_user():
    user_service = UserService()
    user_service.create_user(
        uow,
        request.json["username"],
        request.json["email"],
    )
    return "OK", 201


@app.route("/user/<userid>/update", methods=["PUT"])
def update_user(userid: int):
    user_service = UserService()
    upd_user = user_service.update_user(
        uow,
        userid,
        request.json.get("username"),
        request.json.get("email"),
    )
    if upd_user:
        return jsonify(upd_user), 200
    else:
        return "User not found", 400


@app.route("/user/<userid>/delete", methods=["DELETE"])
def delete_user(userid: int):
    user_service = UserService()
    user_service.delete_user(
        uow,
        userid,
    )
    return "OK", 200

@app.route("/users", methods=["GET"])
def get_users_pagination():
    users = all_users(uow)

    return users, 200
