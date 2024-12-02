from service.uow import AbstractUnitOfWork
from domain import entity
from datetime import datetime


class UserService:
    def create_user(self, uow: AbstractUnitOfWork, username: str, email: str = None):
        user = entity.User(username=username, email=email)
        with uow:
            uow.users.add(user)
            uow.commit()

    def update_user(
        self, uow: AbstractUnitOfWork, oid: int, username: str, email: str
    ) -> entity.User:
        with uow:
            user = entity.User(oid=oid, username=username, email=email)
            upd_user = uow.users.update(user)
            uow.commit()
            return upd_user

    def delete_user(self, uow: AbstractUnitOfWork, oid: int):
        with uow:
            uow.users.delete(oid)
            uow.commit()

    def get_user(self, uow: AbstractUnitOfWork, oid: int) -> entity.User:
        with uow:
            user = uow.users.get(oid)
            return user
