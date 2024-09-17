from flask import Blueprint, g, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, current_user
from ..database.db import get_db
from ..database.user_db_requests import get_ranking



bp = Blueprint('ranking', __name__)


@bp.route('/ranking')
@login_required
def ranking(username):    
    db = get_db()
    ranking = get_ranking(db)
    #NEED RENDER TEMPLATE
    return render_template('', ranking = ranking)