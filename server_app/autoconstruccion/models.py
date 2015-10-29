from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __init__(self, name=None, description=None):
        self.parse( {'name': name, 'description': description} );

    def __repr__(self):
        return "Project: {} \nDescription: {}".format(self.name, self.description)

    def parse(self, data):
        self.name = data['name']
        self.description = data['description']

    @classmethod
    def from_dict(cls, data):
        cls.name = data['name']
        cls.description = data['description']
        return cls


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    tel = db.Column(db.String(9), nullable=False)

    def __init__(self, full_name, email, tel):
        self.full_name = full_name
        self.email = email
        self.tel = tel

    def __repr__(self):
        text = "Usuario: \t{}\n\t\temail: {}\n\t\ttelefono: {}"
        return text.format(self.full_name, self.email, self.tel)
