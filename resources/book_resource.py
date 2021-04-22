from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data.books import Book
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('author', required=True)
parser.add_argument('description', required=True)
parser.add_argument('content', required=True)


def abort_if_book_not_found(book_id):
    session = db_session.create_session()
    books = session.query(Book).get(book_id)
    if not books:
        abort(404, message=f'Book {book_id} not found')


class BookResource(Resource):
    def get(self, book_id):
        abort_if_book_not_found(book_id)
        session = db_session.create_session()
        book = session.query(Book).get(book_id)
        return jsonify({'book': book.to_dict(only=('title', 'author', 'content', 'description'))})

    def put(self):
        pass

    def delete(self):
        pass


class BookListResource(Resource):
    def get(self):
        session = db_session.create_session()
        books = session.query(Book).all()
        return jsonify({'books': [item.to_dict(only=('title', 'author', 'content')) for item in books]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        book = Book(title=args['title'],
                    author=args['author'],
                    description=args['description'],
                    content=args['content'])
        session.add(book)
        session.commit()
        return jsonify({'success': 'OK'})
