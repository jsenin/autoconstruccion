from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms import StringField, FileField, validators, DateField
from autoconstruccion.validators import remove_not_numbers


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


class UserForm(Form):
    full_name = TextField('Full name', [
                          validators.Required(),
                          validators.Length(min=3, max=255)],
                          description='Your full name')

    email = TextField('Email', [
                      validators.Required(),
                      validators.email('Email not valid')])

    phone_number = TextField('Phone number',
                             [],
                             filters=(remove_not_numbers,))

    habilities = TextAreaField('Describe your habilities', [])

    availability = TextAreaField('Describe your availability', [])

    tools = TextAreaField('Do you have some usefull tools? What?', [])

    materials = TextAreaField('Do you have some usefull materials? What?', [])
