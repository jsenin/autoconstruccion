from flask import Blueprint
from flask import flash
from flask import render_template, request, redirect, url_for

from autoconstruccion.models import Project, db
from autoconstruccion.models import User
from autoconstruccion.web.forms import ProjectForm
from autoconstruccion.web.forms import UserForm

bp = Blueprint('web', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='static/web')


@bp.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)



@bp.route('projects')
def project_index():
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects)


@bp.route('projects/add', methods=['GET', 'POST'])
def project_add():
    if request.method == 'POST':
        project_form = ProjectForm(request.form)
        project = Project()
        project_form.populate_obj(project)
        if project_form.image.has_file():
            project.image = request.files['image']
        else:
            project.image = None
        db.session.add(project)
        db.session.commit()
    else:
        project_form = ProjectForm()

    projects = Project.query.all()
    return render_template('projects/add.html', projects=projects, form=project_form)


@bp.route('projects/<int:project_id>', methods=['GET'])
def project_view(project_id):
    project= Project.query.get(project_id)
    return render_template('projects/view.html', project=project)


@bp.route('projects/edit/<int:project_id>', methods=['GET', 'POST'])
def project_edit(project_id):

    project = Project.query.get(project_id)

    if request.method == 'POST':
        project_form = ProjectForm(request.form)
        project_form.populate_obj(project)
        if project_form.image.has_file():
            project.image = request.files['image']
        else:
            project.image = None
        db.session.commit()

    return render_template('projects/edit.html', project=project)


@bp.route('projects/<int:project_id>/join', methods=['GET', 'POST'])
def project_join(project_id):
    project = Project.query.get(project_id)
    form = UserForm(request.form)

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()

        user.projects.append(project)
        db.session.commit()

        flash('Success', 'success')
        return redirect(url_for('web.project_view',project_id=project_id))

    return render_template('projects/join.html', project=project, form=form)


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
