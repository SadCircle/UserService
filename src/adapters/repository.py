import abc
from adapters import orm
from domain import entity


class AbstractRepository(abc.ABC):
    """
    Класс, добавляющий слой абстракции,
    инкапсулирующий в себе всё,
    что относится к способу хранения данных.

    Назначение: Разделение бизнес-логики от деталей реализации слоя доступа к данным

    """

    def add(self, username: str, email: str):
        self._add(username, email)

    def get(self, oid) -> entity.User:
        user = self._get(oid)
        return user

    def update(self, upd_user: entity.User) -> entity.User:
        return self._update(upd_user)

    def delete(self, oid: int):
        user = self._get(oid)
        if user:
            self._delete(user)

    def get_by_username(self, username: str) -> entity.User:
        user = self._get_by_username(username)
        return user

    @abc.abstractmethod
    def _add(self, user: entity.User):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, oid: int) -> entity.User:
        raise NotImplementedError

    @abc.abstractmethod
    def _update(self, upd_user: entity.User) -> entity.User:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, user: entity.User):
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_username(self, username: str) -> entity.User:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    """
    Конкретная реализация репозитория
    для взаимодействия с sqlalchemy
    """

    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, username, email):
        user_dto = orm.UserORM(username=username, email=email)
        self.session.add(user_dto)

    def _get(self, oid):
        user = self.session.get(orm.UserORM, oid)
        return user.to_entity() if user else None

    def _update(self, upd_user):
        cur_user: orm.UserORM = self.session.get(orm.UserORM, upd_user.oid)
        if not cur_user:
            return None
        cur_user.username = upd_user.username
        cur_user.email = upd_user.email
        return cur_user.to_entity()

    def _delete(self, user):
        user = self.session.get(orm.UserORM, user.oid)
        self.session.delete(user)

    def _get_by_username(self, username):
        return (
            self.session.query(orm.UserORM)
            .filter(
                orm.UserORM.username == username,
            )
            .first()
        )
