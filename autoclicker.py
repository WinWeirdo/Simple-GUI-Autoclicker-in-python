import pyautogui
import keyboard
import time
import threading
import tkinter as tk
from tkinter import messagebox

# Configure pyautogui to have minimal pause between actions.
pyautogui.PAUSE = 0
# Global flag for auto clicking.
running = False

# Create a threading event to stop the clicker thread when exiting.
stop_event = threading.Event()

def clicker():
    #Function that simulates auto clicking while running is True.
    while not stop_event.is_set():
        try:
            # Retrieve CPS (clicks per second) from the GUI
            current_cps = int(cps_var.get())
            # Avoid division by zero.
            interval = 1 / current_cps if current_cps > 0 else 0.05
        except Exception:
                interval = 0.05  # fallback interval
        if keyboard.is_pressed('esc'):
            on_exit()
        if running:
            pyautogui.click()
            time.sleep(interval)
        else:
            time.sleep(0.2)

def toggle_clicking():
    global running
    if running:
        a = 1
    else:
        time.sleep(3)
    """Toggles the clicking state and updates the button text."""
    running = not running
    if running:
        start_stop_btn.config(text="Stop Clicking")
    else:
        start_stop_btn.config(text="Start Clicking")

def on_exit():
    #Exit the program.
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        stop_event.set()  # Signal the thread to stop.
        root.destroy()
# Info message.
tk.messagebox.showinfo("Info", "There is 3 second delay between clicking start clicking and it starting clicking also you could use F6 button to start the autoclicker and stop it. You could also use ESC button to exit.")
# Set up the main GUI
root = tk.Tk()
root.title("Auto Clicker")

# Configure window size and layout.
root.geometry("300x150")
root.resizable(False, False)

# Buttons for controlling the auto clicker.
# Label and Entry for CPS configuration.
cps_var = tk.StringVar(value="20")
tk.Label(root, text="CPS (clicks per second):").pack(pady=(20, 5))
cps_entry = tk.Entry(root, textvariable=cps_var, width=10, justify='center')
cps_entry.pack()

start_stop_btn = tk.Button(root, text="Start Clicking", width=20, command=toggle_clicking)
start_stop_btn.pack(pady=5)


exit_btn = tk.Button(root, text="Exit", width=20, command=on_exit)
exit_btn.pack(pady=10)

# Start/stop F6 key.
keyboard.add_hotkey('F6', toggle_clicking)

# Start the clicker function in a separate daemon thread.
clicker_thread = threading.Thread(target=clicker, daemon=True)
clicker_thread.start()

# Override the window close protocol // what?
root.protocol("WM_DELETE_WINDOW", on_exit)

# Start the GUI loop.
root.mainloop()

# Unhook hotkeys after exiting the main loop.
keyboard.unhook_all_hotkeys()
