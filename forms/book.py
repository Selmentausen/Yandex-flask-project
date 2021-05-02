from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField
from wtforms import SelectMultipleField, IntegerField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    release_date = DateField('Release date')
    is_user_author = BooleanField('Are you the Author?')
    price = IntegerField('Cost')
    stock = IntegerField('Stock')
    content = FileField('Content',
                        validators=[FileAllowed(['pdf', 'txt'], message='File should be (.txt, .pdf)')])
    categories = SelectMultipleField('Categories', choices=[], coerce=int)
    image = FileField('Cover', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp'], message='File should be (.jpg, .jpeg, .png, .gif, .bmp)')])
    submit = SubmitField('Add')
