from service import uow
from sqlalchemy import text

def all_users(uow: uow.SqlAlchemyUnitOfWork, count: int = 10, offset: int = 0):
    with uow:
        results = uow.session.execute(
            text("""SELECT id, username, email, registration_date FROM User"""),
        ).fetchall()[offset:offset+count]
        print(results)
    return [dict(r) for r in results]


