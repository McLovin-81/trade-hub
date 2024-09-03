
"""
This module contains the API endpoints for the application.

Endpoints:

"""

from flask import jsonify, request

def get_data():
    data = {
        "message": "Hello, World!",
        "status": "success"
    }
    return jsonify(data)

def receive_data():
    received_data = request.json
    print(f"Received data: {received_data}")
    response = {
        "status": "received",
        "received_data": received_data
    }
    return jsonify(response)
