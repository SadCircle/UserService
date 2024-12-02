from collections import defaultdict
from datetime import date
from typing import Dict, List
import pytest
import bootstrap
from service.user import UserService
from adapters import repository
from service import uow
from domain import entity


class FakeRepository(repository.AbstractRepository):
    oid_counter = 1
    def __init__(self, users):
        super().__init__()
        self._users = set(users)

    def _add(self, user):
        user.oid=self.oid_counter
        self._users.add(user)
        self.oid_counter+=1

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
        user = self._get(oid)
        if user:
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

        # new_user = entity.User(
        #     oid=1,
        #     username='test'
        # )
        user_service.create_user(
            uow,
            username='test'
        )
        assert uow.users.get_by_username('test') is not None
        assert uow.committed




