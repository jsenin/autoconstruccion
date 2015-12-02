from flask import Blueprint, render_template


bp = Blueprint('admin', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='static/admin')


@bp.route('/', methods=['GET', 'POST'])
def admin_index():
    return render_template('admin/index.html')
