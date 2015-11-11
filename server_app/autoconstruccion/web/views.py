from flask import Blueprint
from flask import flash
from flask import render_template, request, redirect, url_for

from autoconstruccion.models import Project, db
from autoconstruccion.models import User

from autoconstruccion.forms import UserForm

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
def user_index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@bp.route('users/add', methods=['GET', 'POST'])
def user_add():

    form = UserForm(request.form)
    if request.method == 'POST':

        if (form.validate()):
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.user_index'))

        flash('Data not valid, please review the fields')

    return render_template('users/add.html', form=form)



@bp.route('users/<int:user_id>', methods=['GET','POST'])
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


    return render_template('users/edit.html',form=form, user_id=user_id)
