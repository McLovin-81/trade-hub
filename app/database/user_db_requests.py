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
    SELECT id, symbol, quantity, amount, price, t_timestamp 
    FROM transactionHistory t
    JOIN user u on t.user_id = u.id
    WHERE u.username = ?
    HAVING quantity > 0        
    ''')
    transaction_history = db.execute(query, (username)).fetchall()
    #START HERE FOR TRANSACTION AND RANKING
    """user_profit = {
            "username": username,
            "profit": profit
        }
        
        # Füge das Dictionary zur Bestenliste hinzu
        ranking.append(user_profit)
    
    # Sortiere die Liste nach Profit in absteigender Reihenfolge
    ranking = sorted(ranking, key=lambda x: x['profit'], reverse=True)"""

def get_user_transactions(username, db):
    #db = get_db()
    query = (
        "SELECT t.symbol, SUM(t.quantity) AS total_quantity, AVG(t.price) AS average_price "
        "FROM transactionHistory t "
        "JOIN user u ON t.user_id = u.id "
        "WHERE u.username = ? "
        "GROUP BY t.symbol "
        "HAVING total_quantity > 0"
    )
    #print( db.execute(query, (username,)).fetchall()[1][0]  ) #ITERATION OVER [0][0] to[x][y] TO get the name in 0:0, number in 0:1 Oterwise only pointer.

    ''' 
    stocks ={ [
                {   "symbol": "",
                    "name"  : "",
                    "amount": "",
                    "price" : "",
                    "total" : "",
                    "profit": ""
                },
            ]}   
        loop über symbole aus dem query result ( db.execute(query, (username,)).fetchall()[i][j]).
        i ist hierbei das symbol
        und wende get_stock_info(symbol) an.
        nehme aus dem dictionary aus dem return den key:currentPrice und daraus den value.Füge ihn
        dem stocks an der stelle price hinzu.
        aus der datenbank nehme amount heraus
        Nutze price und amount, um den gesamtwert (akkurat) zu kalkulieren und füge ihn dann stocks
        an der Stelle total hinzu.
    '''
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
        return 0  # Kein Durchschnittspreis vorhanden, daher kein Profit berechenbar.
    
    # Berechne das Verhältnis von current_price zu average_price
    profit_ratio = current_price / average_price
    
    # Subtrahiere 1, um den Prozentsatz über oder unter dem Durchschnitt zu erhalten
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
    user_query = '''SELECT username from user'''
    userlist=[] 
    usernames = db.execute(user_query).fetchall()
    for user in usernames:
        userlist.append(user[0])
    
    
