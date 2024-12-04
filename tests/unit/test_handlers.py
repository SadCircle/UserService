from collections import defaultdict
from datetime import date
from typing import Dict, List
import pytest
import bootstrap
from service.user import UserService
from adapters import repository
from service import uow
from domain import entity
from core.exceptions import ApplicationException


class FakeRepository(repository.AbstractRepository):
    oid_counter = 1

    def __init__(self, users):
        super().__init__()
        self._users = set(users)

    def _add(self, username: str, email: str):
        oid = self.oid_counter
        user = entity.User(oid=oid, username=username, email=email)
        self._users.add(user)
        self.oid_counter += 1
        return user

    def _get(self, oid):
        return next((u for u in self._users if u.oid == oid), None)

    def _update(self, upd_user):
        cur_user = self._get(upd_user.oid)
        if not cur_user:
            return None
        cur_user.username = upd_user.username
        cur_user.email = upd_user.email
        return cur_user

    def _delete(self, oid):
        user = self.get(oid)
        self._users.remove(user)

    def _get_by_username(self, username):
        return next(
            (u for u in self._users if u.username == username),
            None,
        )


class FakeUnitOfWork(uow.AbstractUnitOfWork):
    def __init__(self):
        self.users = FakeRepository([])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


def bootstrap_test_app():
    return bootstrap.bootstrap(
        uow=FakeUnitOfWork(),
    )


class TestAddUser:
    def test_for_new_user(self):
        uow = bootstrap_test_app()
        user_service = UserService()

        user = user_service.create_user(uow, username="test1")
        assert uow.users.get_by_username("test1").oid == user.oid
        assert uow.committed

    def test_user_already_exist(self):
        uow = bootstrap_test_app()
        user_service = UserService()

        user_service.create_user(uow, username="test")
        try:
            user_service.create_user(uow, username="test")
        except ApplicationException:
            pass
        else:
            raise Exception


class TestDeleteUser:
    def test_delete_user(self):
        uow = bootstrap_test_app()
        user_service = UserService()

        user = user_service.create_user(uow, username="test2")
        user_service.delete_user(uow, user.oid)

        assert uow.users.get_by_username("test2") is None

    def test_delete_not_existed_user(self):
        uow = bootstrap_test_app()
        user_service = UserService()

        try:
            user_service.delete_user(uow, 1)
        except ApplicationException:
            pass
        else:
            raise Exception


class TestUpdateUser:
    def test_update_user(self):
        uow = bootstrap_test_app()
        user_service = UserService()

        user = user_service.create_user(uow, username="test2")
        user_service.update_user(uow, user.oid, username="test3")

        assert uow.users.get_by_username("test2") is None
        assert uow.users.get_by_username("test3") is not None

    def test_update_used_username(self):
        uow = bootstrap_test_app()
        user_service = UserService()

        user = user_service.create_user(uow, username="test2")
        _ = user_service.create_user(uow, username="test3")
        try:
            user_service.update_user(uow, user.oid, username="test3")
        except ApplicationException:
            pass
        else:
            raise Exception
