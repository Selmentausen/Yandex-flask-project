import sqlalchemy
import datetime
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

books_in_user_cart = sqlalchemy.Table('books_in_user_cart',
                                      SqlAlchemyBase.metadata,
                                      sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
                                      sqlalchemy.Column('book', sqlalchemy.Integer, sqlalchemy.ForeignKey('books.id')))

books_to_categories = sqlalchemy.Table('books_to_categories',
                                       SqlAlchemyBase.metadata,
                                       sqlalchemy.Column('categories', sqlalchemy.Integer,
                                                         sqlalchemy.ForeignKey('categories.id')),
                                       sqlalchemy.Column('book', sqlalchemy.Integer, sqlalchemy.ForeignKey('books.id')))


class Book(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, index=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_path = sqlalchemy.Column(sqlalchemy.String, default='img/placeholder.png')
    file_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    release_date = sqlalchemy.Column(sqlalchemy.Date, default=datetime.datetime.now().date())
    author_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('authors.id'), nullable=True)
    author = orm.relation('Author', back_populates='books')
