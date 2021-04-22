from flask import Flask
from data import db_session
from flask_restful import Api
from resources import user_resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/data.sqlite')
    api.add_resource(user_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(user_resource.UsersListResource, 'api/users')
    app.run()


if __name__ == '__main__':
    main()
