from datetime import datetime, timedelta
import random
from werkzeug.security import check_password_hash, generate_password_hash

def create_dummy_data(db):
    """
    Function to create and insert dummy user data, accounts, and transactions into the database.
    """

    # List of dummy users with (username, email, password, isAdmin) format
    users = [
        ('pipe', 'alice.wonder@example.com', '12345678', False),
        ('bob_builder', 'bob.builder@example.com', 'bobpass123', False),
        ('charlie_brown', 'charlie.brown@example.com', 'charliepass123', False),
        ('daisy_duke', 'daisy.duke@example.com', 'daisypass123', False)
    ]

    # Insert users into the database
    for username, email, password, isAdmin in users:
        # Hash the password for security
        hashed_password = generate_password_hash(password)
        db.execute('''
            INSERT INTO user (username, email, password, isAdmin) 
            VALUES (?, ?, ?, ?)
        ''', (username, email, hashed_password, isAdmin))

    db.commit()

    # Fetch user IDs after insertion for further account and transaction operations
    user_ids = {
        'pipe': db.execute("SELECT id FROM user WHERE username = 'pipe'").fetchone()[0],
        'bob_builder': db.execute("SELECT id FROM user WHERE username = 'bob_builder'").fetchone()[0],
        'charlie_brown': db.execute("SELECT id FROM user WHERE username = 'charlie_brown'").fetchone()[0],
        'daisy_duke': db.execute("SELECT id FROM user WHERE username = 'daisy_duke'").fetchone()[0]
    }

    # Insert accounts linked to each user
    for user_id in user_ids.values():
        db.execute('''
            INSERT INTO account (user_id)
            VALUES (?)
        ''', (user_id,))
    
    db.commit()

    # Fetch available product symbols
    symbols = [row['symbol'] for row in db.execute('SELECT symbol FROM product').fetchall()]

    # Generate and insert transactions for each user
    transactions = []
    for user_id in user_ids.values():
        for _ in range(5):  # Generate 5 transactions per user
            symbol = random.choice(symbols)
            quantity = random.randint(1, 20)
            price = round(random.uniform(100, 2000), 2)  # Random price between 100 and 2000, rounded to 2 decimals
            amount = round(price * quantity, 2)  # Total amount
            timestamp = datetime.now() - timedelta(days=random.randint(1, 100))  # Random date within last 100 days
            
            # Append transaction to the list
            transactions.append((user_id, symbol, quantity, amount, price, timestamp))
    
    # Insert transactions into the database
    db.executemany('''
        INSERT OR IGNORE INTO transactionHistory (user_id, symbol, quantity, amount, price, t_timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', transactions)
    
    db.commit()

    print("Dummy data for users, accounts, and transaction history successfully inserted!")