from wtforms import Form, TextAreaField
from wtforms import StringField, FileField, validators, DateField


class ProjectForm(Form):

    name = StringField('name', [
        validators.DataRequired(),
        validators.Length(min=3, max=255)
    ])
    description = TextAreaField('description', [validators.Length(min=5)])
    start_date = DateField('start_date', format='%d/%m/%Y')
    end_date = DateField('end_date', format='%d/%m/%Y')
    location = StringField('location', [validators.DataRequired()])
    phone_number = StringField('phone_number')
    image = FileField('image')
