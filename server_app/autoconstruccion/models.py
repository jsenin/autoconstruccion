from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    image = db.Column(db.LargeBinary)
    location = db.Column(db.String(200), nullable=False)
    contact_phone = db.Column(db.String(15), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    manager = db.relationship('User', uselist=False)

    def __repr__(self):
        return "Project: {} \nDescription: {}".format(self.name, self.description)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(9), nullable=False)
    abilities = db.Column(db.Text(), nullable=True)
    availability = db.Column(db.Text(), nullable=True)
    tools = db.Column(db.Text(), nullable=True)
    materials = db.Column(db.Text(), nullable=True)

    def __repr__(self):
        text = "User: \t{}\n\t\tEmail: {}\n\t\tPhone Number: {}"
        return text.format(self.full_name, self.email, self.phone_number)
