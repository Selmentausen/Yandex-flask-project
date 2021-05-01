from flask import jsonify
from flask_restful import reqparse, abort, Resource
from data.categories import Category
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)


def abort_if_book_not_found(category_id):
    session = db_session.create_session()
    books = session.query(Category).get(category_id)
    if not books:
        abort(404, message=f'Category {category_id} not found')


class CategoryResource(Resource):
    def get(self, category_id):
        abort_if_book_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Category).get(category_id)
        return jsonify({'category': category.to_dict(only=('name',))})


class CategoryListResource(Resource):
    def get(self):
        session = db_session.create_session()
        categories = session.query(Category).all()
        return jsonify({'categories': [item.to_dict(only=('name',)) for item in categories]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        category = Category(name=args['name'])
        session.add(category)
        session.commit()
        return jsonify({'success': 'OK'})
