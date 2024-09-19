import yfinance as yf
from app.database.db import get_db


def get_products():
    db = get_db()
    product_list = []  
    query = ('''SELECT * FROM product''')
    products = db.execute(query).fetchall()
    for product in products:
        product ={product[0] : product[1]}
        product_list.append(product)
    return product_list 

def get_stock_news(product_list):
    news_data = {}  

    for product in product_list:
        
        for id, ticker in product.items():
            stock = yf.Ticker(ticker)
            news = stock.news  
            news_data[ticker] = news  
    return news_data 