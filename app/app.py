
from flask import Flask
from .routes import *
from .api import *

def create_app():
    app = Flask(__name__)

    # Register routes for HTML pages
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/legend', 'legend', legend)

    # Register API endpoints
    app.add_url_rule('/api/data', 'get_data', get_data, methods=['GET'])
    app.add_url_rule('/api/data', 'receive_data', receive_data, methods=['POST'])

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    