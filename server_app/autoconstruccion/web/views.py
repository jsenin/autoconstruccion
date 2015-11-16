from io import BytesIO
from flask import Blueprint
from flask import flash, send_file, abort
from flask import render_template, request, redirect, url_for

from autoconstruccion.models import Project, db
from autoconstruccion.models import User
from autoconstruccion.web.forms import ProjectForm
from autoconstruccion.web.forms import UserForm

from .utils import get_image_from_file_field

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
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        project = Project()
        project_form.populate_obj(project)
        project.image = get_image_from_file_field(project_form.image, request)
        db.session.add(project)
        db.session.commit()

    projects = Project.query.all()
    return render_template('projects/add.html', projects=projects, form=project_form)


@bp.route('projects/<int:project_id>', methods=['GET', 'POST'])
def project_edit(project_id):

    project = Project.query.get(project_id)

    if request.method == 'POST':
        project_form = ProjectForm(request.form)
        project_form.populate_obj(project)
        project.image = get_image_from_file_field(project_form.image, request)
        db.session.commit()

    return render_template('projects/edit.html', project=project)


@bp.route('projects/<int:project_id>/image.jpg')
def get_project_image(project_id):
    project = Project.query.get(project_id)
    if project.image:
        return send_file(BytesIO(project.image), mimetype='image/jpg')
    else:
        #return default image
        abort(404)


@bp.route('users', methods=['GET', 'POST'])
def user_index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@bp.route('users/add', methods=['GET', 'POST'])
def user_add():

    form = UserForm(request.form)
    if request.method == 'POST':

        if form.validate():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.user_index'))

        flash('Data not valid, please review the fields')
    return render_template('users/add.html', form=form)


@bp.route('users/<int:user_id>', methods=['GET', 'POST'])
def user_edit(user_id):

    user = User.query.get(user_id)
    form = UserForm(request.form, user)

    if request.method == 'POST':
        if form.validate():
            form.populate_obj(user)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.user_index'))

        flash('Data not valid, please review the fields')
    return render_template('users/edit.html', form=form, user_id=user_id)
