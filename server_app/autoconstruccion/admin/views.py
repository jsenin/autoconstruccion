from flask import Blueprint, render_template
from autoconstruccion.models import Project, db, Event, User
#Esto lo he cambiado yo(sergio espero no haber metido la pata) 

bp = Blueprint('admin', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='static/admin')


@bp.route('/', methods=['GET', 'POST'])
def admin_index():
	projects = Project.query.all()
	return render_template('admin/index.html', projects=projects)
