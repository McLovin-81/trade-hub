import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

from localStoragePy import localStoragePy


def set_symbol_localStorage(symbol):
    if symbol != None:
        localStorage = localStoragePy('app', 'json')  # or 'json', 'text'
        localStorage.setItem('Symbol', symbol)
        

def get_symbol_localStorage():
    localStorage = localStoragePy('app', 'json')
    return localStorage.getItem('Symbol')

def get_start_date(date):

    if date == '1y':
        start_date = datetime.today() - timedelta(days=365)
    elif date == '1m':  
        start_date = datetime.today() - timedelta(days=30)
    else:  # Standard: 1 Year
        start_date = datetime.today() - timedelta(days=365)
    
    return start_date.strftime('%Y-%m-%d')



def get_graph_info(symbol, startTime):
    symbol = get_symbol_localStorage()
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = get_start_date(startTime)
    return symbol, start_date, end_date

#symbol is NONE. ANFANG HIER! in print().


def create_stock_graph(symbol, start_date, end_date):
    symbol = symbol
    start_date = start_date
    end_date = end_date
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    
    fig = go.Figure(data=[go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=symbol)])
    
    config = {
    'displayModeBar': False,  # Entfernt die gesamte Toolbar
    # 'displaylogo': False,   # Entfernt das Plotly-Logo
    # 'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'],  # Entfernt spezifische Buttons
    # 'showTips': False       # Zeigt keine Tooltips an
    }
    return fig.to_html(full_html=False, config = config)

def get_stock_info(symbol):
    if symbol == None:
        symbol=get_symbol_localStorage()
        get_stock_info(symbol)
    else:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get("longName")
        sector = info.get("sector")
        currency = info.get("currency")
        currentPrice = info.get("currentPrice")
        previousClose = info.get("previousClose")
        return {
            "name": name,
            "sector": sector,
            "currency": currency,
            "currentPrice": round(currentPrice, 2),
            "previousClose": previousClose
        }

def calculate_stock_changes(stock_info):
    if stock_info == None:
        stock_info = get_stock_info(get_symbol_localStorage())
        calculate_stock_changes(stock_info)
    else:
        change = stock_info['currentPrice'] - stock_info['previousClose']
        percentage_change = (change / stock_info['previousClose']) * 100
        stock_info['change'] = f"{change:.2f}"
        stock_info['percentage_change'] = f"{percentage_change:.2f}"

        return stock_info



