from flask import Blueprint
from flask import render_template, request

from autoconstruccion.models import Project, db

bp = Blueprint('web', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='static/web')


@bp.route('/', methods=['GET', 'POST'])
def index():
 
    
    if request.method == 'POST':
        project = Project()
        project.parse(request.form)
        db.session.add(project)
        db.session.commit()

    projects = Project.query.all()
    return render_template('Projects/add.html', projects=projects)
