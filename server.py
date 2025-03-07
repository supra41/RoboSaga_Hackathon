# flask_server.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/employee/<employee_id>', methods=['GET'])
def get_state_times(employee_id):
    """Returns the open, closed, and away times for a specific employee."""
    # Access the times from the eye detection module for the given employee_id
    return jsonify({
        'employee_id': employee_id,
        'hello': 'world'
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)