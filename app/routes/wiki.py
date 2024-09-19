
from flask import (
    Blueprint, redirect, render_template,
    request, url_for
)


bp = Blueprint('info_sites', __name__)


@bp.route('/wiki', endpoint='wiki')
def index():
    
    return render_template('wiki.html')