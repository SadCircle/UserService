from typing import Optional
from datetime import datetime
from sqlalchemy import MetaData, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from domain import entity


metadata = MetaData()
BaseORM = declarative_base(metadata=metadata)


class UUIDOidMixin:
    oid: Mapped[int] = mapped_column(
        name="id", primary_key=True, unique=True, autoincrement=True
    )


class UserORM(UUIDOidMixin, BaseORM):
    __tablename__ = "User"
    username: Mapped[str]
    email: Mapped[Optional[str]]
    registration_date: Mapped[datetime] = mapped_column(
        default=func.now(),
        server_default=func.now(),
    )

    def to_entity(self) -> entity.User:
        return entity.User(
            oid=self.oid,
            username=self.username,
            email=self.email,
            registration_date=self.registration_date,
        )

    @classmethod
    def from_entity(cls, entity: entity.User) -> "UserORM":
        return UserORM(
            oid=entity.oid,
            username=entity.username,
            email=entity.email,
            registration_date=entity.registration_date,
        )
