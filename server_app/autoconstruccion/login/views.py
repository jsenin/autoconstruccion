from flask import Blueprint, redirect
import flask
from flask_login import login_required, login_user, logout_user
import itsdangerous
from autoconstruccion.models import db, User
from .forms import LoginForm, RegisterForm

bp = Blueprint('login', __name__)


@bp.route('register', methods=['GET', 'POST'])
def register():
    # This go here until we found a better place
    def get_activation_link(user):
        serializer = itsdangerous.URLSafeSerializer(secret_key=flask.current_app.config['SECRET_KEY'])
        ACTIVATION_SALT = flask.current_app.config['USER_ACTIVATION_SALT']
        return flask.url_for('activate', code=serializer.dumps(user.user_id, salt=ACTIVATION_SALT))

    login_form = LoginForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():

        # test duplication of user mail -> make in a better way in future, form validator
        user = User.query.filter_by(email=login_form.email.data).one_or_none()
        if user:
            flask.flash('email already in use by another user.', 'error')
            register_form.email.errors.append('email already in use by another user.')
            return flask.render_template('login/login.html', login_form=login_form, reg_for=register_form)

        new_user = User()
        register_form.populate_obj(new_user)
        new_user.store_password_hashed(register_form.password.data)

        # send activation email

        # new user is all right, persist
        db.session.add(new_user)
        db.session.commit()

        login_user(user)

        flask.flash('User registered successfully.', 'success')

        # redirect to user data fill....
        return flask.redirect(flask.url_for('web.index'))
    return flask.render_template('login/login.html', login_form=login_form, reg_for=register_form)


def next_is_valid(next_url):
    # Exclude some urls here -> return False
    return True


@bp.route('login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()
    if login_form.validate_on_submit():
        # Return one user filter by email or None. Raise an exception if more than one user is find.
        user = User.query.filter_by(email=login_form.email.data).one_or_none()
        if not (user and user.test_password(login_form.password.data)):
            flask.flash('Incorrect user email or password.', 'error')
            return flask.render_template('login/login.html', login_form=login_form, reg_for=register_form)

        login_user(user)
        flask.flash('Logged in successfully.', 'success')

        next_url = flask.request.args.get('next')
        # next_is_valid should check if the user has valid permission to access the `next` url
        if not next_is_valid(next_url):
            return flask.abort(400)

        return flask.redirect(next_url or flask.url_for('web.index'))
    return flask.render_template('login/login.html', login_form=login_form, reg_for=register_form)


@bp.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(flask.url_for('web.index'))


@bp.route('activate/<code>')
def activate(code):
    serializer = itsdangerous.URLSafeSerializer(secret_key=flask.current_app.config['SECRET_KEY'])
    ACTIVATION_SALT = flask.current_app.config['USER_ACTIVATION_SALT']
    try:
        user_id = serializer.loads(code, salt=ACTIVATION_SALT)
    except itsdangerous.BadSignature:
        flask.abort(404)
    # user is find, activate it
    user = db.session.query(User).get(user_id)
    user.activate()
    db.session.commit()
