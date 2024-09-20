from datetime import datetime, timedelta
from decimal import Decimal
import random
from app.graph_utilities.search_validation import dax_aktien
from app.graph_utilities.graph_utils import get_stock_info
from werkzeug.security import generate_password_hash
def create_admin(db):


    # Einfügen von mehr Dummy-Benutzern
    users = [
        ('admin', 'turnschuhadmin@gmail.com', generate_password_hash('admin123'), True) #admin123
    ]

    for user in users:
        db.execute('''
        INSERT INTO user (username, email, password, isAdmin) 
        VALUES (?, ?, ?, ?)
        ''', user)
    db.commit()
    


    admin_id = db.execute("SELECT id FROM user WHERE username = 'admin'").fetchone()[0]

    newAccounts = [admin_id]
    for account in newAccounts:
        db.execute('''
        INSERT INTO account (user_id, status_id)
        VALUES (?, ?)
        ''', (account, random.randint(0, 1))
        )
    db.commit()

