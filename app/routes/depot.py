
from flask import Blueprint, render_template
from .auth import login_required  # Import the login_required decorator


bp = Blueprint('dep', __name__, url_prefix='/user')


@bp.route('/depot')
@login_required
def depot():
    return render_template('depot/depot.html')