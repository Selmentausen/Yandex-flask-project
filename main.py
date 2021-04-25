import os
from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.books import Book
from forms.user import RegisterForm, LoginForm
from forms.book import BookForm
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user
from resources import user_resource, book_resource
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')

login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/')
def main_page():
    session = db_session.create_session()
    books = session.query(Book).all()
    return render_template('index.html', books=books)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.create_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        book = Book(
            title=form.title.data,
            author=form.author.data,
            description=form.description.data,
            content=form.content.data,
        )
        if form.image.data:
            image_path = f'img/{secure_filename(form.image.data.filename)}'
            request.files[form.image.name].save(os.path.join(app.config['UPLOAD_FOLDER'], image_path))
            book.image_path = image_path
        session.add(book)
        session.commit()
        return redirect('/')
    else:
        return render_template('add_book.html', title='Добавление книги', form=form)


@app.route('/view_book/<int:book_id>')
def view_book(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    return render_template('view_book.html', book=book)


def main():
    db_session.global_init('db/data.sqlite')
    api.add_resource(user_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(user_resource.UsersListResource, '/api/users')
    api.add_resource(book_resource.BookResource, '/api/books/<int:book_id>')
    api.add_resource(book_resource.BookListResource, '/api/books/')
    app.run()


if __name__ == '__main__':
    main()
