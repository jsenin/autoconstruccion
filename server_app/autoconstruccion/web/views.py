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


@bp.route('projects')
def project_index():
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects)


@bp.route('projects/add', methods=['GET', 'POST'])
def project_add():
    if request.method == 'POST':
        project = Project()
        project.parse(request.form)
        db.session.add(project)
        db.session.commit()

    projects = Project.query.all()
    return render_template('projects/add.html', projects=projects)


@bp.route('projects/<int:project_id>', methods=['GET','POST'])
def project_edit(project_id):

    project = Project.query.get(project_id)

    if request.method == 'POST':
        project.parse(request.form)
        db.session.commit()

    return render_template('projects/edit.html',project=project)


@bp.route('users', methods=['GET', 'POST'])
def users():
    return "Users"


@bp.route('users/<int:user_id>')
def get_user(user_id):
    return "user: {}".format(user_id)
