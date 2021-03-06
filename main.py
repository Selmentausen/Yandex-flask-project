import os

import wtforms_json

from PIL import Image
from flask import Flask, render_template, redirect, request, abort, send_file
from data import db_session
from data.users import User
from data.books import Book
from data.authors import Author
from data.categories import Category
from forms.user import RegisterForm, LoginForm, BalanceForm
from forms.book import BookForm, BookEditForm
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from resources import user_resource, book_resource, categories_resource
import uuid


wtforms_json.init()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


def resize_and_save_image(filename):
    name, extension = filename.split('.')
    file_path = f'{uuid.uuid4().hex}.{extension}'
    request.files['image'].save(os.path.join(app.config['UPLOAD_FOLDER'], 'img', file_path))
    im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], 'img', file_path))
    im = im.resize((300, 400))
    im.save(os.path.join(app.config['UPLOAD_FOLDER'], 'img', file_path))
    return file_path


def save_file(filename):
    name, extension = filename.split('.')
    file_path = f'{uuid.uuid4().hex}.{extension}'
    request.files['content'].save(os.path.join(app.config['UPLOAD_FOLDER'], 'books', file_path))
    return file_path


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter((User.email == form.username.data.lower()) |
                                          (User.username == form.username.data.lower())).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect password or login",
                               form=form)
    return render_template('login.html', title='Sing in', form=form)


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
            return render_template('register.html', title='Sing up',
                                   form=form,
                                   message="Passwords not matching")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter((User.email == form.email.data) |
                                      (User.username == form.username.data)).first():
            return render_template('register.html', title='Sing up',
                                   form=form,
                                   message="Username/email exists")
        # noinspection PyArgumentList
        user = User(
            username=form.username.data.lower(),
            email=form.email.data.lower(),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            about=form.about.data,

        )
        user.create_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Sing up', form=form)


@app.route('/')
def main_page():
    session = db_session.create_session()
    books = session.query(Book).all()
    if current_user.is_authenticated:
        bought_books = session.query(User).get(current_user.id).bought_books
    else:
        bought_books = []
    return render_template('index.html', books=books, bought_books=bought_books, title='BookQ')


@app.route('/user_page/<int:user_id>')
def user_page(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    books = user.bought_books
    books.extend(session.query(Book).filter(Book.author_id == current_user.author.id).all())
    if user != current_user:
        abort(403)
    return render_template('user_page.html', user=user, bought_books=books)


@login_required
@app.route('/book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    session = db_session.create_session()
    form.categories.choices = [(category.id, category.name) for category in
                               session.query(Category).order_by(Category.name).all()]
    if form.validate_on_submit():
        user = session.query(User).get(current_user.id)

        # noinspection PyArgumentList
        book = Book(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            release_date=form.release_date.data
        )

        if form.is_user_author:
            author = session.query(Author).get(user.author_id)
            if not author:
                # noinspection PyArgumentList
                author = Author(first_name=current_user.first_name, last_name=current_user.last_name)
                user.author = author
            book.author = author
        # Save image and/or book file to server if provided
        if form.image.data:
            image_path = resize_and_save_image(form.image.data.filename)
            book.image_path = image_path
        if form.content.data:
            file_path = save_file(form.content.data.filename)
            book.file_path = file_path
        session.merge(book)
        session.commit()
        return redirect('/')
    return render_template('add_book.html', title='Add book', form=form, header='Add book')


@login_required
@app.route('/book_delete/<int:book_id>')
def delete_book(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    if not book:
        abort(404)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'img', book.image_path))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'books', book.file_path))
    session.delete(book)
    session.commit()
    return redirect('/')


@login_required
@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    form = BookEditForm()
    session = db_session.create_session()
    form.categories.choices = [(category.id, category.name) for category in
                               session.query(Category).order_by(Category.name).all()]
    if request.method == "GET":
        book = session.query(Book).get(book_id)
        if not book:
            abort(404)
        form.title.data = book.title
        form.description.data = book.description
        form.release_date.data = book.release_date
        form.price.data = book.price
        form.stock.data = book.stock

    if form.validate_on_submit():
        book = session.query(Book).get(book_id)
        book.title = form.title.data
        book.description = form.description.data
        book.release_date = form.release_date.data
        book.stock = form.stock.data
        if form.is_user_author:
            author = session.query(Author).get(current_user.author_id)
            if not author:
                # noinspection PyArgumentList
                author = Author(first_name=current_user.first_name, last_name=current_user.last_name)
                current_user.author = author
            book.author = author
            book.author_id = current_user.id
        # Save image and/or book file to server if provided
        if form.image.data:
            image_path = resize_and_save_image(form.image.data.filename)
            book.image_path = image_path
        if form.content.data:
            file_path = save_file(form.content.data.filename)
            book.file_path = file_path
        session.merge(book)
        session.commit()
        return redirect(f'/view_book/{book.id}')
    return render_template('add_book.html', form=form, title='Edit book', header='Edit Book')


@app.route('/view_book/<int:book_id>')
def view_book(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    if current_user.is_authenticated:
        bought_books = session.query(User).get(current_user.id).bought_books
    else:
        bought_books = []
    if not book:
        abort(404)
    return render_template('view_book.html', book=book, bought_books=bought_books)


@login_required
@app.route('/add_book_to_cart/<int:book_id>')
def add_book_to_cart(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    user = session.query(User).get(current_user.id)
    if not book:
        abort(404)
    if book in user.books_in_cart:
        return redirect('/')
    user.books_in_cart.append(book)
    session.merge(user)
    session.commit()
    return redirect('/')


@login_required
@app.route('/delete_book_from_cart/<int:book_id>')
def delete_book_from_cart(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    user = session.query(User).get(current_user.id)
    user.books_in_cart.remove(book)
    session.merge(user)
    session.commit()
    return redirect(request.referrer)


@login_required
@app.route('/user_cart/<int:user_id>')
def user_cart(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    books = user.books_in_cart
    return render_template('user_cart.html', title='Shopping cart', books_in_cart=books)


@login_required
@app.route('/checkout/<int:user_id>')
def checkout(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if sum([book.price for book in user.books_in_cart]) > user.balance:
        return render_template('user_cart.html', title='Shopping cart', books_in_cart=user.books_in_cart,
                               message='Not enough balance')
    for book in user.books_in_cart:
        user.balance -= book.price
        book.stock -= 1
        user.bought_books.append(book)
        user.books_in_cart.remove(book)
    session.merge(user)
    session.commit()
    return render_template('user_cart.html', title='Shopping cart', books_in_cart=user.books_in_cart,
                           message='Purchased successfully')


@login_required
@app.route('/empty_cart/<int:user_id>')
def empty_cart(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    user.books_in_cart.clear()
    session.merge(user)
    session.commit()
    return redirect(f'/user_cart/{user_id}')


@login_required
@app.route('/download_book/<int:book_id>')
def download_book(book_id):
    session = db_session.create_session()
    book = session.query(Book).get(book_id)
    file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], 'books', book.file_path)
    return send_file(file_path, as_attachment=True)


@login_required
@app.route('/add_balance/<int:user_id>', methods=['GET', 'POST'])
def add_balance(user_id):
    form = BalanceForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.balance += form.amount.data
        session.commit()
        return redirect('/')
    return render_template('add_balance.html', title='Balance', form=form)


def main():
    db_session.global_init('db/data.sqlite')
    api.add_resource(user_resource.UsersResource, '/api/users/<int:user_id>')
    api.add_resource(user_resource.UsersListResource, '/api/users')
    api.add_resource(book_resource.BookResource, '/api/books/<int:book_id>')
    api.add_resource(book_resource.BookListResource, '/api/books/')
    api.add_resource(categories_resource.CategoryResource, '/api/categories/<int:category_id>')
    api.add_resource(categories_resource.CategoryListResource, '/api/categories')
    app.run()


if __name__ == '__main__':
    main()
