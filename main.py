from flask import Flask, jsonify
import sys
import os

app = Flask(__name__)

# Get the current version from the project configuration
def get_version():
    # In a real implementation, this could read from package metadata
    return "0.1.0"

@app.route('/api/version', methods=['GET'])
def api_version():
    """Return the current version of the service"""
    version_info = {
        'version': get_version(),
        'service': 'umami-badge',
        'python_version': sys.version,
        'environment': os.environ.get('ENVIRONMENT', 'development')
    }
    return jsonify(version_info)

@app.route('/api/health', methods=['GET'])
def api_health():
    """Return the health status of the service"""
    health_status = {
        'status': 'healthy',
        'service': 'umami-badge',
        'version': get_version()
    }
    return jsonify(health_status)

@app.route('/api/status', methods=['GET'])
def api_status():
    """Return a combined status response"""
    status_info = {
        'status': 'running',
        'version': get_version(),
        'service': 'umami-badge',
        'timestamp': __import__('datetime').datetime.now().isoformat()
    }
    return jsonify(status_info)

def main():
    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == "__main__":
    main()
