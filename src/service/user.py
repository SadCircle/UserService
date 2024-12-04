from service.uow import AbstractUnitOfWork
from core.exceptions import ApplicationException
from domain import entity


class UserService:
    """Сервис, предоставляющий CRUD методы по отношеению к пользователю
    """
    def create_user(
        self, uow: AbstractUnitOfWork, username: str, email: str = None
    ) -> entity.User:
        """Создает нового пользователя если (username) свободен и вызывает ApplicationException в противном случае"""
        with uow:
            exist_user = uow.users.get_by_username(username)
            if exist_user:
                raise ApplicationException("User already exist")
            user = uow.users.add(username=username, email=email)
            uow.commit()
            return user

    def update_user(
        self, uow: AbstractUnitOfWork, oid: int, username: str = None, email: str = None
    ) -> entity.User:
        """Обновляет данные пользователя если выбранный (username) свободен и вызывает ApplicationException в противном случае"""
        with uow:
            exist_user = uow.users.get_by_username(username)
            if exist_user:
                raise ApplicationException("Username is used")
            user = entity.User(oid=oid, username=username, email=email)
            upd_user = uow.users.update(user)
            uow.commit()
            return upd_user

    def delete_user(self, uow: AbstractUnitOfWork, oid: int):
        """Удаляет пользователя если он существует вызывает ApplicationException в противном случае"""
        with uow:
            exist_user = uow.users.get(oid)
            if not exist_user:
                raise ApplicationException("User does not exist")
            uow.users.delete(oid)
            uow.commit()

    def get_user(self, uow: AbstractUnitOfWork, oid: int) -> entity.User:
        """Получет пользователя по object id"""
        with uow:
            user = uow.users.get(oid)
            return user
