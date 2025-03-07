from pynput import keyboard, mouse
from datetime import datetime

# Log file to store activity
log_file = "activity_log.txt"

# Function to log activity
def log_activity(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        file.write(f"[{timestamp}] {event}\n")
    print(f"[{timestamp}] {event}")  # Print to console

# Keyboard event handlers
def on_key_press(key):
    try:
        log_activity(f"Key Pressed: {key.char}")
    except AttributeError:
        log_activity(f"Special Key Pressed: {key}")

def on_key_release(key):
    log_activity(f"Key Released: {key}")
    if key == keyboard.Key.esc:
        return False  # Stop listener when ESC is pressed

# Mouse event handlers
def on_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    log_activity(f"Mouse {action} at ({x}, {y}) with {button}")

def on_scroll(x, y, dx, dy):
    log_activity(f"Mouse Scrolled at ({x}, {y}) {'Up' if dy > 0 else 'Down'}")

def on_move(x, y):
    log_activity(f"Mouse Moved to ({x}, {y})")

# Start keyboard and mouse listeners
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as keyboard_listener, \
    mouse.Listener(on_click=on_click, on_scroll=on_scroll, on_move=on_move) as mouse_listener:
    keyboard_listener.join()
    mouse_listener.join()