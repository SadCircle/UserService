from adapters.orm import UserORM
from datetime import datetime
from domain.entity import User
from service import uow
from sqlalchemy import select, func


def all_users(
    uow: uow.SqlAlchemyUnitOfWork, count: int = 10, page: int = 0, offset: int = 10
) -> list[User]:
    """Выводит всех пользователей с наложением пагинации"""
    with uow:
        stmt = select(UserORM)
        users_orm = uow.session.scalars(
            stmt,
        ).fetchall()[page * offset : offset * page + count]

        return [user_orm.to_entity() for user_orm in users_orm]


def get_users_by_period(
    uow: uow.SqlAlchemyUnitOfWork, from_date: datetime, to_date: datetime
) -> int:
    """Выводит число пользователей за определенный период регистрации"""
    with uow:
        stmt = (
            select(func.count(UserORM.oid))
            .where(UserORM.registration_date >= from_date)
            .where(UserORM.registration_date <= to_date)
        )
        user_count: int = uow.session.scalars(
            stmt,
        ).fetchall()
        
        return user_count


def get_top_by_username_length(uow: uow.SqlAlchemyUnitOfWork, count: int) -> list[User]:
    """Выводит (count) пользователей с самым длинными username"""
    with uow:
        stmt = select(UserORM).order_by(func.char_length(UserORM.username).desc())
        users_orm = uow.session.scalars(
            stmt,
        ).fetchall()[:count]

        return [user_orm.to_entity() for user_orm in users_orm]


def get_domain_percent_usage(uow: uow.SqlAlchemyUnitOfWork, domen: str) -> float:
    """Выводит долю пользователей с адресом электронной почты, зарегестрированном в домене (domen)"""
    with uow:
        stmt1 = select(func.count(UserORM.oid))
        stmt2 = select(func.count(UserORM.oid)).where(UserORM.email.like(f"%{domen}"))
        all_user_count = uow.session.scalars(
            stmt1,
        ).one()
        domain_users_count = uow.session.scalars(
            stmt2,
        ).one()

        return float(domain_users_count) / float(all_user_count)
