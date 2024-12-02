from service import  uow


def bootstrap(
    uow: uow.AbstractUnitOfWork = uow.SqlAlchemyUnitOfWork()
) -> uow.AbstractUnitOfWork:

    return uow
