from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField
from wtforms import validators

from autoconstruccion.web.validators import remove_not_numbers


class ProjectForm(Form):

    name = StringField('name', [validators.DataRequired(), validators.Length(min=3, max=255) ])
    description = TextAreaField('description', validators=[validators.Length(min=5)])
    start_date = DateField('start_date', format='%d/%m/%Y', validators=[validators.DataRequired()])
    end_date = DateField('end_date', format='%d/%m/%Y', validators=[validators.DataRequired()])
    location = StringField('location', validators=[validators.DataRequired()])
    contact_phone = StringField('phone_number', validators=[validators.DataRequired()])
    image = FileField('image', validators=[FileAllowed(['jrp', 'png'], 'Only jpg or png images please.')])

class UserForm(Form):
    full_name = StringField('Full name', [validators.DataRequired(), validators.Length(min=3, max=255)],
                            description='Your full name')
    email = StringField('Email', [validators.DataRequired(), validators.email('Email not valid')])
    phone_number = StringField('Phone number', filters=(remove_not_numbers,))
    abilities = TextAreaField('Describe your abilities', [])
    availability = TextAreaField('Describe your availability', [])
    tools = TextAreaField('Do you have some useful tools? What?', [])
    materials = TextAreaField('Do you have some useful materials? What?', [])
