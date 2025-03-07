import time
import datetime
import afk_checks.window_tracker as window_tracker
from afk_checks import eye_tracker
from collections import defaultdict
from time import sleep
from collections import defaultdict
from afk_checks.voice_tracker import VoiceTracker


# Constants
AFK_THRESHOLD = 300  # seconds (5 minutes) of inactivity to be considered AFK
CHECK_INTERVAL = 1  # seconds between checks
PRINT_INTERVAL = 60  # seconds between activity reports
EMPLOYEE_ID=1

# Global variables
last_input_time = time.time()
window_time = defaultdict(float)
current_window = None
current_window_start = time.time()
afk_start_time = None
is_afk = False
total_afk_time = 0

def get_active_window_title():
    """Get the title of the currently active window."""
    monitor = window_tracker()
    return monitor
    

def check_user_activity():
    """Check if there was any keyboard or mouse activity."""
    data = eye_tracker.return_data()
    eye_tracker.reset_data()
    
    return data

def check_voice_activity():
    status = VoiceTracker.get_speaking_status()
    if(status==0):
        return {"SPEAKING"}
    else:
        return {"NOT SPEAKING"}


def main():
    """Main function to run the activity monitoring."""
    print(f"Starting activity monitoring for Employee ID: {EMPLOYEE_ID}")
    print(f"AFK threshold set to {AFK_THRESHOLD} seconds")
    my_map = defaultdict(int)

    while True:
        sleep(CHECK_INTERVAL)
        my_map[get_active_window_title()] += 1
        # Destructure and increment all values
        for key, value in check_user_activity().items():
            my_map[key] += value  # Increment existing values
        
        my_map[check_voice_activity()] += 1    
    
        

        

if __name__ == "__main__":
    main()