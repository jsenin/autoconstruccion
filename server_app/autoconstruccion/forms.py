from wtforms import Form, TextAreaField
from wtforms import TextField, validators


class ProjectForm(Form):

    name = TextField('name', [
        validators.Required(),
        validators.Length(min=3, max=255)
    ])
    description = TextAreaField('description', [validators.Length(min=5)])
