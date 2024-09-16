from app.graph_utilities.graph_utils import get_stock_info
from flask import jsonify
#from app.database.db import get_db AS LONG AS USED IN DB.PY

#from ..database.db import get_db

def get_user_id(username, db):
    query = (
        '''
        SELECT id FROM user WHERE username = ?
        '''
     ) 
    return db.execute(query, (username,)).fetchone()[0] 

def get_transaction_history(username,db):
    query = ('''
    SELECT t.id, t.symbol, t.quantity, t.amount, t.price, t.t_timestamp 
    FROM transactionHistory t
    JOIN user u on t.user_id = u.id
    WHERE u.username = ?       
    ''')
    transaction_history = {} 
    transactions_db = db.execute(query, (username,)).fetchall()
    for transaction in transactions_db:
        transaction_id = transaction[0]
        symbol = transaction[1]
        quantity = transaction[2]
        amount = transaction[3]
        price = transaction[4]
        timestamp = transaction[5]
        
        
        if symbol not in transaction_history:
            transaction_history[symbol] = []
        
        transaction_history[symbol].append({
            'id': transaction_id,
            'quantity': quantity,
            'amount': amount,
            'price': price,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return transaction_history
        
    

def get_user_transactions(username, db):
    #db = get_db()
    query = (
        """SELECT t.symbol, SUM(t.quantity) AS total_quantity, AVG(t.price) AS average_price 
        FROM transactionHistory t 
        JOIN user u ON t.user_id = u.id 
        WHERE u.username = ? 
        GROUP BY t.symbol 
        HAVING total_quantity > 0"""
    )
    #print( db.execute(query, (username,)).fetchall()[1][0]  ) 
    #ITERATION OVER [0][0] to[x][y] TO get the name in 0:0, number in 0:1 Oterwise only pointer.
    return db.execute(query, (username,)).fetchall()

def get_user_balance(username, db):
    #db = get_db()
    query_balance = (
        "SELECT balance " 
        "FROM account "
        "WHERE user_id = (SELECT id FROM user WHERE username = ?) "
    )
    result = str(db.execute(query_balance, (username,)).fetchone()[0] ) #NEEDS TO BE A STRING TO GET IT RETURNED PROPERLY
    
    return result

def process_transactions(transactions):
    stocks = [] 

    for row in transactions:
        symbol = row[0]
        total_quantity = row[1]
        average_price = row[2]

        # Hole aktuelle Infos zum Symbol
        stock_info = get_stock_info(symbol)
        current_price = stock_info["currentPrice"]

        # Berechne den Gesamtwert und den Profit
        total_value = round(total_quantity * current_price, 2)
        profit = calculate_profit(current_price, average_price)

        # Erstelle das Dictionary für diese Aktie
        stock_dict = {
            "symbol": symbol,
            "name"  : stock_info["name"], 
            "amount": total_quantity,
            "price" : current_price,
            "total" : total_value,
            "profit": profit
        }

        # Füge das Dictionary der Liste hinzu
        stocks.append(stock_dict)
        jsonify(stocks)
    
    return stocks

# Berechnung des Profits (Helferfunktion)
def calculate_profit(current_price, average_price):
    if average_price == 0:
        return 0  
    
    profit_ratio = current_price / average_price
    
    profit_percentage = (profit_ratio - 1) * 100
    return round(profit_percentage, 2)

def get_symbol_transactions(username, symbol, db):
    transactions = process_transactions(get_user_transactions(username, db))
    for stock_dict in transactions:
        if stock_dict["symbol"] == symbol:
            return stock_dict
    return None  

def check_balance(balance, cost):
    if balance - cost > 0:
        return True
    else:
        return False

def update_balance(username, balance, db):
    user_id = get_user_id(username, db)
    db.execute(
                "UPDATE account SET balance = ? WHERE user_id = ?",
                (balance, user_id)
            )
    db.commit()
    
def insert_transaction(username,stock_symbol, quantity,total_cost, price_per_stock, db):
    user_id = get_user_id(username, db)

    db.execute(
                "INSERT INTO transactionHistory (user_id, symbol, quantity, amount, price) VALUES (?, ?, ?, ?, ?)",
                (user_id, stock_symbol, quantity, total_cost, price_per_stock)
            )
    db.commit()

def buy_sell_stock(username, stock_symbol, quantity,ordertype, db):
        
        stock_info = get_stock_info(stock_symbol)
        current_price = stock_info["currentPrice"]
        total_cost = quantity * current_price  
        balance = float(get_user_balance(username, db))
        if ordertype != "sell":
            if check_balance(balance, total_cost):

                
                new_balance = balance - total_cost
                update_balance(username, new_balance, db)

                # Transaktion in die Historie einfügen
                insert_transaction(username,stock_symbol, quantity, total_cost, current_price, db)
                
                return True
            else:
                return False
        else:
            user_quantity = get_symbol_transactions(username, stock_symbol, db)["amount"]
            
            if  user_quantity - quantity >= 0: 
                quantity = quantity * -1
                new_balance = balance + total_cost
                update_balance(username, new_balance, db)
                insert_transaction(username, stock_symbol, quantity, total_cost, current_price, db)
                return True
            else:
                return False
            

def get_ranking(db):
    '''get all users via query. for every user process_transactions(get_user_transaction(username,db))
    the list with dictionaries is there as well as the profit.
    for every dictionary get the profit and add it. last put the user as a value and the sum of profit
    as a value.'''
    userlist=[] 
    ranking = []
    user_query = '''SELECT username from user'''
    usernames = db.execute(user_query).fetchall()
    for user in usernames:
        userlist.append(user[0])

    for user in userlist:
        profit = calculate_total_profit(user, db)
        user_profit = {
                "username": user,
                "profit": profit
            }
        ranking.append(user_profit)
    
    # Sort the ranking list
    ranking = sorted(ranking, key=lambda x: x['profit'], reverse=True)

    current_rank = 1
    for i in range(len(ranking)):
        if i > 0 and ranking[i]['profit'] == ranking[i-1]['profit']:
            # same rank when profit is equal
            ranking[i]['rank'] = ranking[i-1]['rank']
        else:
            ranking[i]['rank'] = current_rank
        
        current_rank += 1 
    print(ranking)
    return ranking

def calculate_total_profit(username, db):
    # Hole die Transaktionen des Benutzers
    transactions = process_transactions(get_user_transactions(username, db))    
    
    total_profit = 0
    
    # Summiere den Profit über alle Aktien hinweg
    for stock in transactions:
        total_profit += stock["profit"]
    return round(total_profit, 2)  
