
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)



# A simple REST API endpoint returning JSON data
@app.route("/api/data", methods=["GET"])
def get_data():
    data = {
        "message": "Hello, World!",
        "status": "succes"
    }
    return jsonify(data)

@app.route("/api/data", methods=["POST"])
def receive_data():
    received_data = request.json
    print(f"Recieved data: {received_data}")
    response = {
        "status": "received",
        "received_data": receive_data
    }
    return jsonify(response)



# Render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/legend')
def legend():
    return render_template('legend.html')

if __name__ == '__main__':
    app.run(debug=True)
