from flask import Blueprint, redirect
import flask
from flask_login import login_required, login_user, logout_user
from autoconstruccion.models import User
from .forms import LoginForm


bp = Blueprint('login', __name__)


def next_is_valid(next_url):
    # Exclude some urls here -> return False
    return True


@bp.route('login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Return one user filter by email or None. Raise an exception if more than one user is find.
        user = User.query.filter_by(email=form.user_mail.data).one_or_none()
        if not user:
            flask.flash('Incorrect user email or password.', 'error')
            return flask.render_template('login.html', form=form)

        login_user(user)

        flask.flash('Logged in successfully.', 'success')

        next_url = flask.request.args.get('next')
        # next_is_valid should check if the user has valid
        # permission to access the `next` url
        if not next_is_valid(next_url):
            return flask.abort(400)

        return flask.redirect(next_url or flask.url_for('web.index'))
    return flask.render_template('login.html', form=form)


@bp.route('logout')
@login_required
def logout():
    logout_user()
    return redirect(flask.url_for('web.index'))
