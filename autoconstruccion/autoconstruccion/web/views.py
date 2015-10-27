from flask import Blueprint
from flask import render_template

from autoconstruccion.models import Project

bp = Blueprint('web', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='static/web')


@bp.route('/')
def hello_world():
    project = Project('proyectito', 'pedazo de proyecto')
    project_text = project.__repr__()
    
    return render_template('index.html', projects=[project])
