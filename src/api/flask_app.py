from datetime import datetime, timedelta
from flask import Flask, request
from service.user import UserService
from core.exceptions import ApplicationException
import bootstrap
from view import (
    all_users,
    get_users_by_period,
    get_top_by_username_length,
    get_domain_percent_usage,
)


app = Flask(__name__)
uow = bootstrap.bootstrap()


@app.route("/user/<userid>", methods=["GET"])
def get_user(userid: int):
    """Выводит данные пользователя

    Args:
        userid (int): id пользователя
    """
    user_service = UserService()
    try:
        user = user_service.get_user(uow, userid)
        if user:
            return user.model_dump_json(), 200
        else:
            return "NOT FOUND", 404
    except ApplicationException as e:
        return e.message, 400


@app.route("/user/add", methods=["POST"])
def add_user():
    """Добавляет пользователя в систему"""
    user_service = UserService()
    try:
        username = request.json["username"]
    except KeyError:
        return "Username required", 400
    email = request.json.get("email")
    try:
        user_service.create_user(
            uow,
            username,
            email,
        )
        return "OK", 201
    except ApplicationException as e:
        return e.message, 400


@app.route("/user/<userid>/update", methods=["PUT"])
def update_user(userid: int):
    """Обнавляет данные пользователя
        Можно обновить username и email

    Args:
        userid (int): id пользователя
    """
    user_service = UserService()
    try:
        upd_user = user_service.update_user(
            uow,
            userid,
            request.json.get("username"),
            request.json.get("email"),
        )
        if upd_user:
            return upd_user.model_dump_json(), 200
        else:
            return "User not found", 400
    except ApplicationException as e:
        return e.message, 400


@app.route("/user/<userid>/delete", methods=["DELETE"])
def delete_user(userid: int):
    """Удаляет пользователя

    Args:
        userid (int): id пользователя
    """
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
    """Выводит всех пользователей с использованием пагинации
    query arg count - число записей
    query arg page - страница
    query arg offset - сдвиг (используется в тестовом режиме)
    """
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
    """Выводит число пользователей, зарегестрированных в последние 7 дней
    """
    users = get_users_by_period(uow, datetime.now() - timedelta(days=7), datetime.now())

    return users, 200


@app.route("/users/longest_username", methods=["GET"])
def get_top_five_users_by_username_lenght():
    """ Выводит топ 5 пользователей с самым длинным (username)
    """
    users = get_top_by_username_length(uow, 5)

    return users, 200


@app.route("/domain", methods=["GET"])
def get_domain_percent_usage_api():
    """Вычисляет долю использования домена (domain) среди всех пользователей
    """
    domain = request.args.get("domain")
    percent = get_domain_percent_usage(uow, domain)

    return str(percent), 200
