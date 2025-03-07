# flask_server.py
from flask import Flask, jsonify
import os
import importlib
import sys
# Add the directory containing eye_detection.py to sys.path
sys.path.append(os.path.join(os.getcwd(), 'python files'))

# Import the eye detection module (assuming it's in the same directory)
eye_detection = importlib.import_module("eye_tracker.py")
pose_detection = importlib.import_module("pose_tracker.py")
app = Flask(__name___)

@app.route('/eye_state_times', methods=['GET'])
def get_state_times():
    """Returns the open, closed, and away times."""
    # Access the times from the eye detection module
    return jsonify({
        'open_time': eye_detection.open_time,
        'closed_time': eye_detection.closed_time,
        'away_time': eye_detection.away_time,
        'standing_time': pose_detection.standing_time,
        'sitting_time': pose_detection.sitting_time,
        'hands_up_time': eye_detection.hands_up_time
    })


# Import the eye detection module (assuming it's in the same directory)



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)