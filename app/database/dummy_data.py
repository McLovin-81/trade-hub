from datetime import datetime, timedelta
from decimal import Decimal
import random
from app.graph_utilities.search_validation import dax_aktien
from app.graph_utilities.graph_utils import get_stock_info
from werkzeug.security import generate_password_hash
def create_dummy_data(db):


    # Einfügen von mehr Dummy-Benutzern
    users = [
        ('pipe', 'alice.wonder@example.com', generate_password_hash('12345678'), False), #alicepass123
        ('bob_builder', 'bob.builder@example.com', generate_password_hash('bobpass123'), False), #bobpass123
        ('charlie_brown', 'charlie.brown@example.com', generate_password_hash('charliepass123'), False), #charliepass123
        ('jackson', 'daisy.duke@example.com', generate_password_hash('12345678'), True) #daisypass123
    ]

    for user in users:
        db.execute('''
        INSERT INTO user (username, email, password, isAdmin) 
        VALUES (?, ?, ?, ?)
        ''', user)
    db.commit()
    

    # .fetchone gets the Tuple from the db. (id,) to get only the value of the first Tuple [0] is needed 
    pipe_id = db.execute("SELECT id FROM user WHERE username = 'pipe'").fetchone()[0] 
     
    bob_id = db.execute("SELECT id FROM user WHERE username = 'bob_builder'").fetchone()[0]
     
    charlie_id = db.execute("SELECT id FROM user WHERE username = 'charlie_brown'").fetchone()[0]
    
    jackson_id = db.execute("SELECT id FROM user WHERE username = 'jackson'").fetchone()[0]

    newAccounts = [pipe_id, bob_id, charlie_id, jackson_id]
    for account in newAccounts:
        db.execute('''
        INSERT INTO account (user_id)
        VALUES (?)
        ''', (account,)
        )
    db.commit()


    # Einfügen von Dummy-Transaktionen
    symbols = list(dax_aktien.values())[:5] 
    transactions = []

    # Generiere Transaktionen für jeden Benutzer
    for user_id in [pipe_id, bob_id, charlie_id, jackson_id]:
        for symbol in symbols:  # 5 Transaktionen pro Benutzer
            symbol = symbol
            quantity = random.randint(1, 20)
            price = get_stock_info(symbol)['currentPrice']
            amount = round(price * quantity,2)
            timestamp = datetime.now()
            transactions.append((user_id, symbol, quantity, amount, price, timestamp))
    
    for transaction in transactions:
        db.execute('''INSERT OR IGNORE INTO transactionHistory (user_id, symbol, quantity, amount, price, t_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', transaction
        )
    db.commit()


    print("Test data created!")
