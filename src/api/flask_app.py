from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from service.user import UserService
from core.exceptions import ApplicationException
import bootstrap
from view import all_users, get_users_by_period, get_top_by_username_length, get_domain_percent_usage


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
    try:
        user_service.create_user(
            uow,
            request.json["username"],
            request.json["email"],
        )
        return "OK", 201
    except ApplicationException as e:
        return e.message, 400


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
    try:
        user_service.delete_user(
            uow,
            userid,
        )
        return "OK", 200
    except ApplicationException as e:
        return e.message, 400


@app.route("/users", methods=["GET"])
def get_users_pagination():
    try:
        if count := request.args.get("count"):
            count = abs(int(count))
        else:
            count = 10
        if page := request.args.get("page"):
            page = abs(int(page))
        else:
            page = 0
        if offset := request.args.get("offset"):
            offset = abs(int(offset))
        else:
            offset = 10
    except ValueError:
        return "Wrong query params", 422
    users = all_users(uow, count, page, offset)

    return users, 200


@app.route("/users/last_week", methods=["GET"])
def get_users_by_last_week():
    users = get_users_by_period(uow, datetime.now() - timedelta(days=7), datetime.now())

    return users, 200



@app.route("/users/longest_username", methods=["GET"])
def get_top_five_users_by_username_lenght():
    users = get_top_by_username_length(uow, 5)

    return users, 200

@app.route("/domain", methods=["GET"])
def get_domain_percent_usage_api():
    domain = request.args.get("domain")
    percent = get_domain_percent_usage(uow, domain)

    return str(percent), 200

