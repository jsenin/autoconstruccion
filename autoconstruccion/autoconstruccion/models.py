from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
