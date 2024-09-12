

def get_user_transactions(username, db):
    #db = get_db()
    query = (
        "SELECT t.symbol, SUM(t.quantity) AS total_quantity "
        "FROM transactionHistory t "
        "JOIN user u ON t.user_id = u.id "
        "WHERE u.username = ? "
        "GROUP BY t.symbol "
        "HAVING total_quantity > 0"
    )
    #print( db.execute(query, (username,)).fetchall()[1][0]  ) #ITERATION OVER [0][0] to[x][y] TO get the name in 0:0, number in 0:1 Oterwise only pointer.
     ''' stocks{  symbol:,
                amount:,
                price:,
                total:,
        } 
    stocks = {  "symbol": "",
                "amount": "",
                "price" : "",
                "total" : "",
            } 
        loop über symbole
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
    
    return result[0] if result else None

def transaction_test():
    return