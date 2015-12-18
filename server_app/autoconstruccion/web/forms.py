from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, validators, PasswordField, BooleanField
from autoconstruccion.web.validators import remove_not_numbers


class ProjectForm(Form):
    name = StringField('Name', validators=[validators.DataRequired(), validators.Length(min=3, max=255)])
    description = TextAreaField('Description', validators=[validators.DataRequired(), validators.Length(min=5)])
    start_date = DateField('Start date', format='%d/%m/%Y', validators=[validators.DataRequired()])
    end_date = DateField('End date', format='%d/%m/%Y', validators=[validators.DataRequired()])
    location = StringField('Location', validators=[validators.DataRequired()])
    contact_phone = StringField('Phone number', filters=(remove_not_numbers,), validators=[validators.DataRequired(), validators.Length(max=9)])
    image = FileField('Image', validators=[FileAllowed(['jpg'], 'Only jpg images please.')])


class UserForm(Form):
    full_name = StringField('Full name', [validators.DataRequired(), validators.Length(min=3, max=255)],
                            description='Your full name')
    email = StringField('Email', [validators.DataRequired(), validators.email('Email not valid')])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6, max=32)])
    phone_number = StringField('Phone number', filters=(remove_not_numbers,), validators=[validators.Length(max=9)])
    is_admin = BooleanField('Is admin?', [])
    abilities = TextAreaField('Describe your abilities', [])
    availability = TextAreaField('Describe your availability', [])
    tools = TextAreaField('Do you have some useful tools? What?', [])
    materials = TextAreaField('Do you have some useful materials? What?', [])


class EventForm(Form):
    name = StringField('Event name', [validators.DataRequired(), validators.Length(min=3, max=255)])
    description = TextAreaField('Describe event', [validators.DataRequired(), validators.Length(min=3, max=255)])
    start_date = DateField('Start event', format='%d/%m/%Y')


class SkillForm(Form):
    name = StringField('Skill name', [validators.DataRequired(), validators.Length(min=3, max=255)])
    description = TextAreaField('Describe skill', [validators.Length(min=5, max=255)])
    image = FileField('Image', validators=[FileAllowed(['jpg'], 'Only jpg images please.')])
