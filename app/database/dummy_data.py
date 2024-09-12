from datetime import datetime, timedelta
import random
def create_dummy_data(db):


    # Einfügen von mehr Dummy-Benutzern
    users = [
        ('alice_wonder', 'alice.wonder@example.com', 'alicepass123', False),
        ('bob_builder', 'bob.builder@example.com', 'bobpass123', False),
        ('charlie_brown', 'charlie.brown@example.com', 'charliepass123', False),
        ('daisy_duke', 'daisy.duke@example.com', 'daisypass123', False)
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
    symbols = ['AAPL', 'GOOGL', 'AMZN']
    transactions = []

    # Generiere Transaktionen für jeden Benutzer
    for user_id in [alice_id, bob_id, charlie_id, daisy_id]:
        for _ in range(5):  # 5 Transaktionen pro Benutzer
            symbol = random.choice(symbols)
            quantity = random.randint(1, 20)
            price = random.uniform(100, 2000)  # Zufälliger Preis
            amount = price * quantity
            timestamp = datetime.now() - timedelta(days=random.randint(1, 100)) # Zufällige vergangene Tage
            transactions.append((user_id, symbol, quantity, amount, price, timestamp))
    
    for transaction in transactions:
        db.execute('''INSERT OR IGNORE INTO transactionHistory (user_id, symbol, quantity, amount, price, t_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', transaction
        )
    db.commit()

    
   

        

    print("Zusätzliche Dummy-Daten für Benutzer und aktualisierte Kontostände erfolgreich eingefügt!")