from flask_login import LoginManager

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from autoconstruccion.models import User
    return User.query.get(user_id)


login_manager.login_view = "login.login"

# Default login flash message
login_manager.login_message = "This view is protected, please log in"
login_manager.login_message_category = "info"
