import pyautogui
from pywinauto import Application
from time import sleep

def get_active_window():
    active_window = pyautogui.getActiveWindow()
    if active_window:
        return active_window.title
    else:
        print("No active window detected")
        return None
    
def get_chrome_tabs():
    try:
        app = Application(backend="uia").connect(title_re=".*Chrome.*")
        windows = app.windows()
        
        chrome_tabs = []
        for win in windows:
            if win.window_text():
                chrome_tabs.append(win.window_text())
                
        return chrome_tabs
    except Exception as e:
        print("Error:", e)
        return []