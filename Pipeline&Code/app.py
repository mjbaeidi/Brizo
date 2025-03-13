from flask import Flask, request, jsonify
import elasticapm
from elasticapm import get_client
from elasticapm.contrib.flask import ElasticAPM
import time
import random
import requests

# Define app version
APP_VERSION = "1.0.0"

app = Flask(__name__)

# Configure Elastic APM
app.config['ELASTIC_APM'] = {
    'SERVICE_NAME': 'flask-apm-test',  # Change this to your service name
    'SECRET_TOKEN': 'test',
    'SERVER_URL': 'http://10.192.127.233:8200',  # Change this to your APM server
    'ENVIRONMENT': 'my-environment',
    'CAPTURE_BODY': 'all',
}

apm = ElasticAPM(app)

@app.route('/')
def home():
    return "Flask APM Test Service Running!"

@app.route('/slow')
def slow_request():
    time.sleep(random.uniform(1, 3))  # Simulate slow request
    return "This was a slow request"

@app.route('/error')
def error_request():
    try:
        1 / 0
    except ZeroDivisionError:
        apm.capture_exception()
        return "Error occurred: Division by zero"

@app.route('/trace', methods=['POST'])
def trace_request():
    data = request.json
    return jsonify({"message": "Received", "data": data})

@app.route('/call-external')
def call_external():
    """Simulate a request to another service and propagate tracing headers"""
    header = {}
    try:
        response = requests.get("https://www.google.com")
        return jsonify({"status": response.status_code, "response": response.text})
    except requests.exceptions.RequestException as e:
        apm.capture_exception()
        return jsonify({"error": str(e)}), 500

@app.route('/version')
def version():
    """Return the current application version"""
    return jsonify({"version": APP_VERSION})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)