from io import BytesIO
from flask import Blueprint, flash, send_file, render_template, request, redirect, url_for, abort
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

    # Don't pass request.form as flask_wtf do it automatically, and
    # if request.form is passed it won't load the images!!!!
    project_form = ProjectForm()

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
    form = ProjectForm(obj=project)

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
        # return default image for a project
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
            return redirect(url_for('web.project_events', project_id=project_id))

        flash('Data not valid, please review the fields')

    return render_template('events/add.html', project_id=project_id, form=form)



@bp.route('projects/<int:project_id>/events/edit', methods=['GET', 'POST'])
def event_edit(project_id):
    form = EventForm(request.form)
    if request.method == 'POST':
        if form.validate():
            event = Event()
            form.populate_obj(event)
            event.project_id = project_id
            db.session.add(event)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.project_events', project_id=project_id))

        flash('Data not valid, please review the fields')

    return render_template('events/edit.html', project_id=project_id, form=form)


@bp.route('projects/<int:project_id>/events/<int:event_id>', methods=['GET'])
def project_event(project_id, event_id):
    conditions = (Event.id == event_id,
                  Event.project_id == project_id)
    event = Event.query.filter(*conditions).first()
    return render_template('events/view.html', event=event) if event else abort(404)


@bp.route('projects/<int:project_id>/events', methods=['GET'])
def project_events(project_id):
    conditions = (Event.project_id == project_id,)
    events = Event.query.filter(*conditions).all()

    return render_template('projects/events.html', events=events, project_id=project_id)

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

@bp.route('project/<int:project_id>/events/<int:event_id>', methods=['GET'])
def event_view():
    events = Event.query.all()
    return render_template('events/view.html', event=event)


@bp.route('events', methods=['GET'])
def event_index():
    events = Event.query.all()
    return render_template('events/index.html', events=events)



@bp.route('admin')
def admin_index():
    return render_template('admin/index.html')
