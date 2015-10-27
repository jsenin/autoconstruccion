from flask import Blueprint

from autoconstruccion.models import Project

bp = Blueprint('web', __name__)


@bp.route('/')
def hello_world():
    project = Project('proyectito', 'pedazo de proyecto')
    project_text = project.__repr__()
    return project_text
