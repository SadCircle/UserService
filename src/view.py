from service import uow
from domain.entity import User
from adapters.orm import UserORM
from sqlalchemy import select

def all_users(uow: uow.SqlAlchemyUnitOfWork, count: int = 10, page: int = 0, offset: int= 10)->list[User]:
    with uow:
        stmt = select(UserORM)
        users_orm = uow.session.scalars(
            stmt,
        ).fetchall()[page*offset:offset*page+count]
        
        return [user_orm.to_entity() for user_orm in users_orm]
    




