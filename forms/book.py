from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField
from wtforms import SelectMultipleField, IntegerField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Титул', validators=[DataRequired()])
    description = TextAreaField('Краткое описание', validators=[DataRequired()])
    release_date = DateField('Время выпуска')
    is_user_author = BooleanField('Вы автор книги?')
    price = IntegerField('Стоимость книги')
    content = FileField('Содержание',
                        validators=[FileAllowed(['pdf', 'txt'], message='Выберите файл в формате (.txt, .pdf)')])
    categories = SelectMultipleField('Категории', choices=[], coerce=int)
    image = FileField('Обложка', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp'], message='Неправильный формат изображения')])
    submit = SubmitField('Добавить')
