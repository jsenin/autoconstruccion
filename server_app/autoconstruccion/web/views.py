from io import BytesIO

from flask import Blueprint, flash, send_file, render_template, request, redirect, url_for

from autoconstruccion.models import Project, db, Event, User
from autoconstruccion.web.forms import ProjectForm, UserForm, EventForm
from .utils import get_image_from_file_field

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

    project_form = ProjectForm(request.form)

    if project_form.validate_on_submit():
        project = Project()
        project_form.populate_obj(project)
        project.image = get_image_from_file_field(project_form.image, request)
        db.session.add(project)
        db.session.commit()

        flash('Project created', 'success')
        return redirect(url_for('web.project_index'))

    return render_template('projects/add.html', form=project_form)


@bp.route('projects/<int:project_id>')
def project_view(project_id):
    project = Project.query.get(project_id)
    return render_template('projects/view.html', project=project)


@bp.route('projects/edit/<int:project_id>', methods=['GET', 'POST'])
def project_edit(project_id):

    project = Project.query.get(project_id)
    form = ProjectForm(request.form, project)

    if form.validate_on_submit():
        project.image = get_image_from_file_field(form.image, request)
        db.session.commit()

        flash('Project edited', 'success')
        return redirect(url_for('web.project_index'))

    return render_template('projects/edit.html', form=form, project_id=project_id)


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
        return redirect(url_for('web.project_view', project_id=project_id))

    return render_template('projects/join.html', project=project, form=form)


@bp.route('projects/<int:project_id>/image')
def get_project_image(project_id):
    project = Project.query.get(project_id)
    if project.image:
        return send_file(BytesIO(project.image), mimetype='image/jpg')
    else:
        # return default image
        return send_file('web/static/img/image_not_found.jpg', mimetype='image/jpg')


@bp.route('projects/<int:project_id>/events/add', methods=['GET', 'POST'])
def event_add(project_id):

    form = EventForm(request.form)
    if request.method == 'POST':

        if form.validate():
            event = Event()
            form.populate_obj(event)
            event.project_id = project_id
            db.session.add(event)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.project_view', project_id=project_id))

        flash('Data not valid, please review the fields')
    return render_template('events/add.html', project_id=project_id, form=form)


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


@bp.route('events', methods=['GET'])
def event_index():
    events = Event.query.all()
    return render_template('events/index.html', events=events)
