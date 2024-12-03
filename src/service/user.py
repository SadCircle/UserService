from service.uow import AbstractUnitOfWork
from core.exceptions import ApplicationException
from domain import entity
from datetime import datetime


class UserService:
    def create_user(self, uow: AbstractUnitOfWork, username: str, email: str = None):
        with uow:
            exist_user =  uow.users.get_by_username(username)
            if exist_user:
                raise ApplicationException("User already exist")
            uow.users.add(username=username, email=email)
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
            exist_user =  uow.users.get(oid)
            if not exist_user:
                raise ApplicationException("User does not exist")
            uow.users.delete(oid)
            uow.commit()

    def get_user(self, uow: AbstractUnitOfWork, oid: int) -> entity.User:
        with uow:
            user = uow.users.get(oid)
            return user
