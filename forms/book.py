from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Тутил', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    description = TextAreaField('Краткое описание', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    image = FileField('Обложка', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp'], message='Неправильный формат изображения')])
    submit = SubmitField('Добавить')
