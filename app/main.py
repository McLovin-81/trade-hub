
"""
This module serves as the entry point for running the Flask application.

It imports the `create_app` function from the `app` package's `__init__.py` file, 
initializes the Flask application, and starts the development server if the script 
is executed directly.

Modules:
    app (module): Contains the `create_app` function used to create the Flask app instance.
"""
import argparse
from __init__ import create_app


app = create_app()




if __name__ == '__main__':
    """
    If this script is executed directly, this block will run the Flask application.
    
    The app will be started in debug mode, which is useful for development, as it provides 
    interactive debugging and reloading on code changes.
    """
    parser = argparse.ArgumentParser(description="Run the Flask application.")
    parser.add_argument('-d', '--dummy', action='store_true',help="Run in dummy mode.")
    parser.add_argument('-p', '--production', action='store_true', help="Run in production mode.")
    parser.add_argument('--port', type=int, default=5000, help="Specify the port to run the server on (default is 5000).")
    parser.add_argument('--host', type=str,default='127.0.0.1', help="Specify the host to run the server on (default is '127.0.0.1').")
    args = parser.parse_args()
    if args.production:
        app.debug = False
        ssl_context = ('instance/certs/cert.pem', 'instance/certs/key.pem')
    elif args.dummy:
        ssl_context = 'adhoc'
    else:
        ssl_context = None
    app.run(host=args.host, port=args.port,ssl_context=ssl_context)
   
