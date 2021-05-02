import os
from PIL import Image

from flask import jsonify
from flask_restful import reqparse, abort, Resource
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from data.books import Book
from data.authors import Author
from data.users import User
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('release_date')
parser.add_argument('is_user_author', required=True)
parser.add_argument('price', type=int, required=True)
parser.add_argument('categories')
parser.add_argument('content', type=FileStorage, location='files', required=True)
parser.add_argument('image', type=FileStorage, location='files', required=True)
parser.add_argument('current_user_id', type=int, required=True)


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
        print(args['image'])
        print(args['content'])

        session = db_session.create_session()
        user = session.query(User).get(args['current_user_id'])
        book = Book(
            title=args['title'],
            description=args['description'],
            price=args['price']
        )
        if args.is_user_author:
            author = session.query(Author).get(user.author_id)
            if not author:
                author = Author(first_name=user.first_name, last_name=user.last_name)
                user.author = author
            book.author = author
            book.author_id = user.id
        # Save image and/or book file to server if provided
        if args['image']:
            image_path = f'img/{secure_filename(args["image"].data.filename)}'
            full_image_path = os.path.join('/static', image_path)
            args['image'].save(full_image_path)
            im = Image.open(full_image_path)
            im = im.resize((75, 100))
            im.save(full_image_path)
            book.image_path = image_path
        if args['content']:
            file_path = f'books/{secure_filename(args["content"].data.filename)}'
            args['content'].save(os.path.join('/static', file_path))
            book.file_path = file_path
        session.merge(book)
        session.commit()
        return jsonify({'success': 'OK'})
