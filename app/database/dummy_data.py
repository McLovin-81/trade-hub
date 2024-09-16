from datetime import datetime, timedelta
from decimal import Decimal
import random
from app.graph_utilities.search_validation import dax_aktien
from app.graph_utilities.graph_utils import get_stock_info
from werkzeug.security import generate_password_hash
def create_dummy_data(db):


    # Einfügen von mehr Dummy-Benutzern
    users = [
        ('alice_wonder', 'alice.wonder@example.com', generate_password_hash('alicepass123'), False), #alicepass123
        ('bob_builder', 'bob.builder@example.com', generate_password_hash('bobpass123'), False), #bobpass123
        ('charlie_brown', 'charlie.brown@example.com', generate_password_hash('charliepass123'), False), #charliepass123
        ('daisy_duke', 'daisy.duke@example.com', generate_password_hash('daisypass123'), False) #daisypass123
    ]

    for user in users:
        db.execute('''
        INSERT INTO user (username, email, password, isAdmin) 
        VALUES (?, ?, ?, ?)
        ''', user)
    db.commit()
    

    # .fetchone gets the Tuple from the db. (id,) to get only the value of the first Tuple [0] is needed 
    alice_id = db.execute("SELECT id FROM user WHERE username = 'alice_wonder'").fetchone()[0] 
     
    bob_id = db.execute("SELECT id FROM user WHERE username = 'bob_builder'").fetchone()[0]
     
    charlie_id = db.execute("SELECT id FROM user WHERE username = 'charlie_brown'").fetchone()[0]
    
    daisy_id = db.execute("SELECT id FROM user WHERE username = 'daisy_duke'").fetchone()[0]

    newAccounts = [alice_id, bob_id, charlie_id, daisy_id]
    for account in newAccounts:
        db.execute('''
        INSERT INTO account (user_id)
        VALUES (?)
        ''', (account,)
        )
    db.commit()

    
    # Aktualisieren von Dummy-Kontoständen
    updated_accounts = [
        (25000, alice_id),
        (30000, bob_id),
        (18000, charlie_id),
        (12000, daisy_id)
    ]
    
    for balance, user_id in updated_accounts:
        db.execute('''
        UPDATE account 
        SET balance = ?
        WHERE user_id = ?
        ''', (balance, user_id))
    db.commit()
    

    # Einfügen von Dummy-Transaktionen
    symbols = list(dax_aktien.values())[:5] 
    transactions = []

    # Generiere Transaktionen für jeden Benutzer
    for user_id in [alice_id, bob_id, charlie_id, daisy_id]:
        for symbol in symbols:  # 5 Transaktionen pro Benutzer
            symbol = symbol
            quantity = random.randint(1, 20)
            price = get_stock_info(symbol)['currentPrice']
            amount = price * quantity
            timestamp = datetime.now()
            transactions.append((user_id, symbol, quantity, amount, price, timestamp))
    
    for transaction in transactions:
        db.execute('''INSERT OR IGNORE INTO transactionHistory (user_id, symbol, quantity, amount, price, t_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', transaction
        )
    db.commit()

    
   

        

    print("Zusätzliche Dummy-Daten für Benutzer und aktualisierte Kontostände erfolgreich eingefügt!")