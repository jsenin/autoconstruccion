from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    image = db.Column(db.BLOB, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    contact_phone = db.Column(db.String(15), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manager = db.relationship('User', uselist=False)

    def __init__(self, name=None, description=None):
        self.parse({'name': name, 'description': description})

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
    phone_number = db.Column(db.String(9), nullable=False)
    habilities = db.Column(db.Text(), nullable=True)
    availability = db.Column(db.Text(), nullable=True)
    tools = db.Column(db.Text(), nullable=True)
    materials = db.Column(db.Text(), nullable=True)


    def __repr__(self):
        text = "User: \t{}\n\t\tEmail: {}\n\t\tPhone Number: {}"
        return text.format(self.full_name, self.email, self.phone_number)
