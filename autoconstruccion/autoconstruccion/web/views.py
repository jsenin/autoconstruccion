from flask import Blueprint
from flask import render_template, request

from autoconstruccion.models import Project, db

bp = Blueprint('web', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='static/web')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        project = Project()
        project.parse(request.form)
        db.session.add(project)
        db.session.commit()
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects)


@bp.route('projects/<int:project_id>')
def get_project(project_id):
    return "Project: {}".format(project_id)


@bp.route('users', methods=['GET', 'POST'])
def users():
    return "Users"


@bp.route('users/<int:user_id>')
def get_user(user_id):
    return "user: {}".format(user_id)
