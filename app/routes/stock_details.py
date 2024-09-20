
from flask import (
    Blueprint, redirect, render_template,
    request, url_for
)
from app.graph_utilities.graph_utils import *
from app.graph_utilities.search_validation import *



bp = Blueprint('stock_page', __name__)


@bp.route('/main', endpoint='main')
def main():
    return render_template('main.html', dax_aktien=dax_aktien)




@bp.route('/detailPage', methods=['GET', 'POST'] )
def detailPage(): 

    symbol = request.form.get('symbol')
    
    set_symbol_localStorage(symbol)
    startTime = request.form.get('startTime', '1y')
    graph_info = get_graph_info(symbol, startTime) 
    graph_html = create_stock_graph(*graph_info)
    stock_info = get_stock_info(symbol)
    stock_info_calculated = calculate_stock_changes(stock_info)
    return render_template('stockWindow.html', symbol=symbol, graph_html=graph_html, stock_info=stock_info_calculated)




