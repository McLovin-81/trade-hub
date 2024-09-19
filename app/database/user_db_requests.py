from app.graph_utilities.graph_utils import get_stock_info
from datetime import datetime
# Get the user_id from the username.
# This function takes a username and a database connection, and returns the user's ID.
def get_user_id(username, db):
    query = (
        '''
        SELECT id FROM user WHERE username = ?
        '''
     ) 
    return db.execute(query, (username,)).fetchone()[0] 


# Get the full transaction history for a user.
# This function retrieves all transactions for a given user from the database, organizing them by stock symbol.
# It returns a dictionary where the keys are stock symbols, and the values are lists of transaction details.
def get_transaction_history(username, db):
    query = ('''
    SELECT t.id, t.symbol, t.quantity, t.amount, t.price, t.t_timestamp 
    FROM transactionHistory t
    JOIN user u on t.user_id = u.id
    WHERE u.username = ?
    ORDER BY t.t_timestamp DESC    
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
            'amount': "{:.2f}".format(amount),
            'price': "{:.2f}".format(price),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return transaction_history


# Get the user's stock transactions grouped by stock symbol.
# This function retrieves the total quantity and average price of each stock that the user has purchased.
# It returns a list of pointer tuples where each tuple contains a stock symbol, total quantity, and average price.
def get_user_transactions(username, db):
    query = (
        """SELECT t.symbol, SUM(t.quantity) AS total_quantity, AVG(t.price) AS average_price 
        FROM transactionHistory t 
        JOIN user u ON t.user_id = u.id 
        WHERE u.username = ? 
        GROUP BY t.symbol 
        HAVING total_quantity > 0"""
    )
    return db.execute(query, (username,)).fetchall()


# Get the balance of the user.
# This function retrieves the current balance of a user's account based on their username.
# It returns the balance as a string.
def get_user_balance(username, db):
    query_balance = (
        "SELECT balance " 
        "FROM account "
        "WHERE user_id = (SELECT id FROM user WHERE username = ?) "
    )
    result = str(db.execute(query_balance, (username,)).fetchone()[0])
    return result


# Process the user's transactions to calculate the stock value and profit.
# This function takes a list of transaction pointer (that need to get the values first), retrieves current stock information, and calculates the profit.
# It returns a list of dictionaries containing stock details, total value, and profit.
def process_transactions(transactions):
    stocks = [] 

    for row in transactions:
        symbol = row[0]
        total_quantity = row[1]
        average_price = row[2]

        stock_info = get_stock_info(symbol)
        current_price = stock_info["currentPrice"]

        total_value = round(total_quantity * current_price, 2)
        profit = calculate_profit(current_price, average_price)

        stock_dict = {
            "symbol": symbol,
            "name"  : stock_info["name"], 
            "amount": total_quantity,
            "price" : "{:.2f}".format(current_price),
            "total" : "{:.2f}".format(total_value),
            "profit": profit
        }

        stocks.append(stock_dict)
    return stocks


# Calculate the profit percentage of a stock.
# This function calculates the percentage profit for a stock based on its current price and the average price paid.
# It returns the profit as a percentage rounded to two decimal places.
def calculate_profit(current_price, average_price):
    if average_price == 0:
        return 0  
    
    profit_ratio = current_price / average_price
    profit_percentage = (profit_ratio - 1) * 100
    return round(profit_percentage, 2)


# Get the transaction details for a specific stock symbol.
# This function retrieves the processed transaction data for a specific stock symbol owned by the user.
# It returns a dictionary with stock details or None if the stock is not found.
def get_symbol_transactions(username, symbol, db):
    transactions = process_transactions(get_user_transactions(username, db))
    for stock_dict in transactions:
        if stock_dict["symbol"] == symbol:
            return stock_dict
    return None  


# Check if the user has enough balance to make a purchase.
# This function compares the user's balance with the cost of a transaction.
# It returns True if the balance is sufficient, otherwise False.
def check_balance(balance, cost):
    if balance - cost > 0:
        return True
    else:
        return False


# Update the user's balance in the database.
# This function updates the account balance for a user in the database.
def update_balance(username, balance, db):
    user_id = get_user_id(username, db)
    db.execute(
                "UPDATE account SET balance = ? WHERE user_id = ?",
                (round(balance, 2), user_id)
            )
    db.commit()


# Insert a new transaction into the transaction history.
# This function adds a record to the transactionHistory table with the details of the stock purchase/sale.
def insert_transaction(username, stock_symbol, quantity, total_cost, price_per_stock, db):
    user_id = get_user_id(username, db)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute(
                "INSERT INTO transactionHistory (user_id, symbol, quantity, amount, price, t_timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, stock_symbol, quantity, total_cost, price_per_stock, timestamp)
            )
    db.commit()


# Buy or sell a stock for the user.
# This function processes a buy or sell order based on the order type and updates the user's balance and transaction history.
# It returns True if the order was successful, otherwise False.
def buy_sell_stock(username, stock_symbol, quantity, ordertype, db):
    stock_info = get_stock_info(stock_symbol)
    current_price = stock_info["currentPrice"]
    total_cost = round(quantity * current_price, 2)
    balance = float(get_user_balance(username, db))
    
    if ordertype != "sell":
        if check_balance(balance, total_cost):
            new_balance = balance - total_cost
            update_balance(username, new_balance, db)
            insert_transaction(username, stock_symbol, quantity, total_cost, current_price, db)
            return True
        else:
            return False
    else:
        user_quantity = get_symbol_transactions(username, stock_symbol, db)["amount"]
        if user_quantity - quantity >= 0: 
            quantity = quantity * -1
            new_balance = balance + total_cost
            update_balance(username, new_balance, db)
            insert_transaction(username, stock_symbol, quantity, total_cost, current_price, db)
            return True
        else:
            return False


# Get the profit ranking of all users.
# This function retrieves the profit ranking of all users by calculating the total profit for each user.
# It returns a sorted list of dictionaries with each user's username, profit, and rank.
def get_ranking(db):
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
    
    ranking = sorted(ranking, key=lambda x: x['profit'], reverse=True)

    current_rank = 1
    for i in range(len(ranking)):
        if i > 0 and ranking[i]['profit'] == ranking[i-1]['profit']:
            ranking[i]['rank'] = ranking[i-1]['rank']
        else:
            ranking[i]['rank'] = current_rank
        current_rank += 1 
    return ranking


# Calculate the total profit for a user.
# This function sums the profit of all stocks held by the user.
# It returns the total profit rounded to two decimal places.
def calculate_total_profit(username, db):
    transactions = process_transactions(get_user_transactions(username, db))    
    total_profit = 0
    
    for stock in transactions:
        total_profit += float(stock["profit"])
    return round(total_profit, 2)  






def get_stock_symbols(query, db):
    # Example implementation
    query = f"%{query}%"
    cursor = db.cursor()
    cursor.execute("""
        SELECT symbol, name FROM product
        WHERE symbol LIKE ? OR name LIKE ?
    """, (query, query))
    results = cursor.fetchall()
    return [{"symbol": row[0], "name": row[1]} for row in results]



def set_useraccount_to_reset(username, db):
    user_id = get_user_id(username, db)
    query = ("""UPDATE account SET status_id = 1 WHERE user_id = ?""")
    db.execute(query, (user_id,))
    db.commit()



def delete_account(username, db):
    user_id = get_user_id(username, db)
    query_delete_user = (
    '''
        DELETE FROM user 
        WHERE id = ?
    ''')
    db.execute(query_delete_user, (user_id,))
    
    db.commit()