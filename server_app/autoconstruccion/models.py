from autoconstruccion import db
import hashlib
import os
HASH_SIZE = 32  # sha256 -> 32 bytes

users_projects = db.Table('users_projects', db.metadata,
                       db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')))

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
    users = db.relationship('User', secondary=users_projects)

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
    projects = db.relationship('Project', secondary=users_projects)

    # Login related properties and methods
    _hashed_password = db.Column(db.Binary(HASH_SIZE), nullable=False)
    _salt = db.Column(db.Binary(HASH_SIZE), nullable=False, default=os.urandom(HASH_SIZE))

    @property
    def hashed_password(self):
        return self._hashed_password

    def _generate_hashed_password(self, password):
        if not self._salt:
            self._salt = os.urandom(HASH_SIZE)
        return hashlib.sha256(self._salt + bytes(password, encoding='utf8')).digest()

    def store_password_hashed(self, password):
        hashed_password = self._generate_hashed_password(password)
        self._hashed_password = hashed_password

    def test_password(self, password):
        password_under_test = self._generate_hashed_password(password)
        return password_under_test == self._hashed_password

    def is_authenticated(self):
        return True

    _active = db.Column(db.Boolean, default=True)

    def is_active(self):
        return self._active

    def activate(self):
        self._active = True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        text = "User: \t{}\n\t\tEmail: {}\n\t\tPhone Number: {}"
        return text.format(self.full_name, self.email, self.phone_number)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    project = db.relationship('Project', backref=db.backref('events'))

    def __repr__(self):
        text = "Event: \t{}\n\t\tDescription: {}\n\t\tDay: {}"
        return text.format(self.name, self.description, self.start_date)


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.LargeBinary)

    def __repr__(self):
        text = "Skill: \t{}\n\t\tDescription: {}"
        return text.format(self.name, self.description)

"""
There could have an inconsistency: An user could have skills in a project where he/she is not signed up
"""
class SkillLevel(db.Model):
    __tablename__ = 'skills_levels'

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)
    level = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        text = "Project_id: {}\n\t\tUser_id: {}\n\t\tSkill_id: {}\n\t\tLevel: {}"
        return text.format(self.project_id, self.user_id, self.skill_id, self.level)