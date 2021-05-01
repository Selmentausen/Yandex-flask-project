import os
from PIL import Image
from flask import Flask, render_template, redirect, request, abort
from data import db_session
from data.users import User
from data.books import Book
from data.categories import Category
from forms.user import RegisterForm, LoginForm
from forms.book import BookForm
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from resources import user_resource, book_resource, categories_resource
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

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
        user = db_sess.query(User).filter((User.email == form.username.data) |
                                          (User.username == form.username.data)).first()
        print(user)
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
        if db_sess.query(User).filter((User.email == form.email.data) |
                                      (User.username == form.username.data)).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            about=form.about.data,

        )
        user.create_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user_page/<int:user_id>')
def user_page(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if user != current_user:
        abort(403)
    return render_template('user_page.html', user=user)


@login_required
@app.route('/book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    session = db_session.create_session()
    form.categories.choices = [(category.id, category.name) for category in session.query(Category).all()]
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data
        )
        if form.is_user_author:
            book.author_id = current_user.id
            book.author_name = current_user.last_name + ' ' + current_user.first_name
        # Save image and/or book file to server if provided
        if form.image.data:
            image_path = f'img/{secure_filename(form.image.data.filename)}'
            request.files[form.image.data.name].save(os.path.join(app.config['UPLOAD_FOLDER'], image_path))
            im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image_path))
            im = im.resize((75, 100    ))
            im.save(os.path.join(app.config['UPLOAD_FOLDER'], image_path))
            book.image_path = image_path
        if form.content.data:
            file_path = f'books/{secure_filename(form.content.data.filename)}'
            request.files[form.content.data.name].save(os.path.join(app.config['UPLOAD_FOLDER'], file_path))
            book.file_path = file_path
        session.add(book)
        session.commit()
        return redirect('/')
    return render_template('add_book.html', title='Добавление книги', form=form)


@login_required
@app.route('/book_delete/<int:book_id>')
def delete_book(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404)
    session.delete(book)
    session.commit()
    return redirect('/')


@login_required
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    form = BookForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        book = db_sess.query(Book).get(book_id)
        if not book:
            abort(404)
        form.title.data = book.title
        form.content.data = book.content
        form.author.data = book.author
        form.description.data = book.description

    if form.validate_on_submit():
        session = db_session.create_session()
        book = session.query(Book).get(book_id)
        if not book:
            abort(404)
        book.title = form.title.data
        book.description = form.description.data
        book.author = form.author.data
        if form.image.data:
            image_path = f'img/{secure_filename(form.image.data.filename)}'
            request.files[form.image.data.name].save(os.path.join(app.config['UPLOAD_FOLDER'], image_path))
            book.image_path = image_path
        session.commit()
        return redirect(f'/view_book/{book.id}')

    return render_template('add_book.html', form=form, title='Изменение книги')


@app.route('/view_book/<int:book_id>')
def view_book(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404)
    return render_template('view_book.html', book=book)


def main():
    db_session.global_init('db/data.sqlite')
    api.add_resource(user_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(user_resource.UsersListResource, '/api/users')
    api.add_resource(book_resource.BookResource, '/api/books/<int:book_id>')
    api.add_resource(book_resource.BookListResource, '/api/books/')
    api.add_resource(categories_resource.CategoryResource, '/api/category/<int:category_id>')
    api.add_resource(categories_resource.CategoryListResource, '/api/category')
    app.run()


if __name__ == '__main__':
    main()
