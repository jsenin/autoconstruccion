from flask import Blueprint, render_template
from autoconstruccion.models import Project

bp = Blueprint('admin', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='static/admin')


@bp.route('/', methods=['GET', 'POST'])
def admin_index():
	projects = Project.query.all()
	return render_template('admin/index.html', projects=projects)
