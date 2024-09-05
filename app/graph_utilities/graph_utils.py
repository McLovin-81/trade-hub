import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

def get_graph_info(symbol):
    symbol = symbol
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    return symbol, start_date, end_date

def create_stock_graph(symbol, start_date, end_date):
    stock = symbol
    start_date = start_date
    end_date = end_date
    print(stock, start_date, end_date)
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    
    fig = go.Figure(data=[go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=symbol)])
    return fig.to_html(full_html=False)
