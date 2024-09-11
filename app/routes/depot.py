#SQL STATEMENTS FOR GETTING THE LIST OF THE USERS BOUGHT ITEMS
#LIST THE ITEMS ON THE USER SITE
#BE ABLE TO SEE INCREMENT OR REDUCTION OF THE VALUE OF THE STOCKS.
# SUM AND GROUP BY ON TRANSACTION HISTORY
#SHOW BALANCE

#USE DUMMY USER

from flask import Blueprint, render_template
from app.database import get_user_transactions, get_user_balance


bp = Blueprint('depot', __name__, url_prefix='/user')

@bp.route('/<username>')
def user_account(username):
    transactions = get_user_transactions(username)
    balance = get_user_balance(username)
    return render_template('user_account.html', transactions=transactions, balance=balance, username=username)