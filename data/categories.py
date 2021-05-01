import sqlalchemy
import datetime
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    books = orm.relation('Book', secondary='books_to_categories', backref='categories')
