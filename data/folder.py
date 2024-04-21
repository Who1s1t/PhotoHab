import sqlalchemy

from .db_session import SqlAlchemyBase


class Folder(SqlAlchemyBase):
    __tablename__ = 'folder'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    folder_path = sqlalchemy.Column(sqlalchemy.String)
