from sqlalchemy.orm import DeclarativeBase

from src.config.connection_config import MySQLConnection


class BaseDao(DeclarativeBase):
    @classmethod
    def execute_statement(cls, statement):
        session = MySQLConnection.get_session()
        # result = session.scalars(statement)
        # return result
        try:
            result = session.scalars(statement)
            return result
        finally:
            session.close()
