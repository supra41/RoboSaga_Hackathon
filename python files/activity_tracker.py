from pynput import keyboard, mouse
from datetime import datetime, timedelta
import json
import os
import time
import logging

# Set up enhanced logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f'activity_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
stats_file = os.path.join(log_dir, f'activity_stats_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')

logging.basicConfig(
    filename=os.path.join(log_dir, f'activity_tracker_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Activity tracking variables
activity_stats = {
    "session_start": datetime.now().isoformat(),
    "session_end": None,
    "keyboard_events": 0,
    "mouse_clicks": 0,
    "mouse_movements": 0,
    "mouse_scrolls": 0,
    "active_periods": [],
    "inactive_periods": []
}

last_activity = datetime.now()
activity_timeout = 60  # seconds to consider user inactive
current_active_start = datetime.now()
is_active = True
keys_pressed = set()  # Track currently pressed keys for combinations
combinations_detected = []

# Function to log activity
def log_activity(event_type, details=""):
    global last_activity, is_active, current_active_start
    
    timestamp = datetime.now()
    
    # Check if we're returning from inactivity
    if not is_active:
        inactive_duration = (timestamp - last_activity).total_seconds()
        activity_stats["inactive_periods"].append({
            "start": last_activity.isoformat(),
            "end": timestamp.isoformat(),
            "duration_seconds": inactive_duration
        })
        logging.info(f"User returned after {inactive_duration:.1f} seconds of inactivity")
        current_active_start = timestamp
        is_active = True
    
    last_activity = timestamp
    
    # Log to file
    with open(log_file, "a") as file:
        file.write(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] [{event_type}] {details}\n")

# Check for inactivity periodically
def check_inactivity():
    global last_activity, is_active, current_active_start
    
    while True:
        time.sleep(5)  # Check every 5 seconds
        now = datetime.now()
        
        if is_active and (now - last_activity).total_seconds() > activity_timeout:
            active_duration = (last_activity - current_active_start).total_seconds()
            activity_stats["active_periods"].append({
                "start": current_active_start.isoformat(),
                "end": last_activity.isoformat(),
                "duration_seconds": active_duration
            })
            logging.info(f"User became inactive after {active_duration:.1f} seconds of activity")
            is_active = False

# Save activity statistics
def save_stats():
    activity_stats["session_end"] = datetime.now().isoformat()
    activity_stats["session_duration_seconds"] = (datetime.now() - datetime.fromisoformat(activity_stats["session_start"])).total_seconds()
    
    # Calculate total active/inactive time
    total_active = sum(period["duration_seconds"] for period in activity_stats["active_periods"])
    total_inactive = sum(period["duration_seconds"] for period in activity_stats["inactive_periods"])
    
    activity_stats["total_active_seconds"] = total_active
    activity_stats["total_inactive_seconds"] = total_inactive
    
    # Add key combinations detected
    activity_stats["key_combinations_detected"] = combinations_detected
    
    try:
        with open(stats_file, 'w') as f:
            json.dump(activity_stats, f, indent=2)
        logging.info(f"Activity statistics saved to {stats_file}")
        print(f"\nActivity statistics saved to {stats_file}")
    except Exception as e:
        logging.error(f"Failed to save activity statistics: {e}")
        print(f"Error saving statistics: {e}")

# Keyboard event handlers
def on_key_press(key):
    try:
        key_char = key.char
        event_type = "KEY_PRESS"
        details = f"Key: {key_char}"
        log_activity(event_type, details)
        activity_stats["keyboard_events"] += 1
        
        # Track key combinations (e.g., Ctrl+C)
        keys_pressed.add(key)
        check_key_combinations()
        
    except AttributeError:
        event_type = "SPECIAL_KEY_PRESS"
        details = f"Key: {key}"
        log_activity(event_type, details)
        activity_stats["keyboard_events"] += 1
        
        # Track key combinations with special keys
        keys_pressed.add(key)
        check_key_combinations()
    
    return True

def on_key_release(key):
    try:
        event_type = "KEY_RELEASE"
        details = f"Key: {key}"
        log_activity(event_type, details)
        
        # Remove from pressed keys
        if key in keys_pressed:
            keys_pressed.remove(key)
        
    except Exception as e:
        logging.error(f"Error in key release: {e}")
    
    if key == keyboard.Key.esc:
        # Save stats before exiting
        if is_active:
            active_duration = (datetime.now() - current_active_start).total_seconds()
            activity_stats["active_periods"].append({
                "start": current_active_start.isoformat(),
                "end": datetime.now().isoformat(),
                "duration_seconds": active_duration
            })
        
        save_stats()
        print_summary()
        return False  # Stop listener

def check_key_combinations():
    """Check for meaningful key combinations"""
    
    # Copy-paste combinations
    if keyboard.Key.ctrl in keys_pressed:
        if keyboard.KeyCode.from_char('c') in keys_pressed:
            detect_combination("Ctrl+C (Copy)")
        elif keyboard.KeyCode.from_char('v') in keys_pressed:
            detect_combination("Ctrl+V (Paste)")
        elif keyboard.KeyCode.from_char('z') in keys_pressed:
            detect_combination("Ctrl+Z (Undo)")
        elif keyboard.KeyCode.from_char('a') in keys_pressed:
            detect_combination("Ctrl+A (Select All)")

def detect_combination(combination):
    """Log detected key combination"""
    timestamp = datetime.now().isoformat()
    combinations_detected.append({
        "combination": combination,
        "timestamp": timestamp
    })
    logging.info(f"Key combination detected: {combination}")
    print(f"Combination detected: {combination}")

# Mouse event handlers
def on_click(x, y, button, pressed):
    action = "MOUSE_PRESS" if pressed else "MOUSE_RELEASE"
    details = f"Position: ({x}, {y}), Button: {button}"
    log_activity(action, details)
    
    if pressed:
        activity_stats["mouse_clicks"] += 1

def on_scroll(x, y, dx, dy):
    direction = "Up" if dy > 0 else "Down"
    details = f"Position: ({x}, {y}), Direction: {direction}"
    log_activity("MOUSE_SCROLL", details)
    activity_stats["mouse_scrolls"] += 1

def on_move(x, y):
    # Reduce logging of mouse movements to avoid excessive logs
    if datetime.now().second % 5 == 0:  # Log once every 5 seconds
        details = f"Position: ({x}, {y})"
        log_activity("MOUSE_MOVE", details)
        activity_stats["mouse_movements"] += 1

def print_summary():
    """Print activity summary to console"""
    print("\n=== Activity Summary ===")
    start_time = datetime.fromisoformat(activity_stats["session_start"])
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"Session duration: {duration:.1f} seconds")
    print(f"Keyboard events: {activity_stats['keyboard_events']}")
    print(f"Mouse clicks: {activity_stats['mouse_clicks']}")
    print(f"Mouse movements: {activity_stats['mouse_movements']}")
    print(f"Mouse scrolls: {activity_stats['mouse_scrolls']}")
    
    active_time = sum(period["duration_seconds"] for period in activity_stats["active_periods"])
    inactive_time = sum(period["duration_seconds"] for period in activity_stats["inactive_periods"])
    
    print(f"Total active time: {active_time:.1f} seconds")
    print(f"Total inactive time: {inactive_time:.1f} seconds")
    print(f"Activity ratio: {(active_time/duration)*100:.1f}%")
    print("========================")

# Start inactivity checker in a separate thread
import threading
inactivity_thread = threading.Thread(target=check_inactivity, daemon=True)
inactivity_thread.start()

print(f"Activity tracking started. Press ESC to stop.")
logging.info("Activity tracking started")

# Start keyboard and mouse listeners
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as keyboard_listener, \
    mouse.Listener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as mouse_listener:
    keyboard_listener.join()
    mouse_listener.join()