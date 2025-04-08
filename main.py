import pyautogui
from pynput import keyboard
from pynput import mouse
import tkinter as tk
import threading


end = keyboard.Key.esc
check = False
x_coord = 0
y_coord = 0
mouseThread = None

def endPress(key, injected):
    global check
    if key == end:
        check = True
        return False

def endPressListener():
    with keyboard.Listener(on_press=endPress) as listener:
        listener.join()


def autoclick(button, interval, x, y):
    endThread = threading.Thread(target=endPressListener)
    endThread.daemon = True
    endThread.start()
    global check
    while True:
        pyautogui.click(button=button, interval=interval, x=x, y=y)
        if check == True:
            check = False
            break
    print("Loop ended")

def findMousePos(x, y, button, pressed):
    global x_coord, y_coord, mouseThread
    if button==mouse.Button.left:
        x_coord, y_coord = x, y
        pos.set(f"Autoclicking Position: ({x_coord}, {y_coord})")
        print(pos.get())
        return False

def mousePosListener():
    print("check")
    with mouse.Listener(on_click=findMousePos) as listener:
        listener.join()

def startMouseListener():
    global mouseThread
    if mouseThread is None or not mouseThread.is_alive():
        mouseThread = threading.Thread(target=mousePosListener)
        mouseThread.daemon = True
        mouseThread.start()
    else:
        print("Mouse thread is already running.")
    

root = tk.Tk()
root.title("Autoclicker Menu")
root.geometry("400x400")

titleLabel = tk.Label(root, text="Autoclicker", font=("Helvetica", 12, "bold"))
titleLabel.pack(pady=20)

endStringVar = tk.StringVar()
endStringVar.set(f"End Key: {end}")
endKeyLabel = tk.Label(root, textvariable=endStringVar)
endKeyLabel.pack(pady=20)

intervalLabel = tk.Label(root, text="Enter the interval between clicks in seconds (minimum of 0.1s)")
intervalLabel.pack(pady=10)
intervalEntry = tk.Entry(root)
intervalEntry.pack(pady=20)
intervalEntry.insert(0, "100")

pos = tk.StringVar()
pos.set(f"Autoclicking Position: ({x_coord}, {y_coord})")
posLabel = tk.Label(root, textvariable = pos)
posLabel.pack(pady=10)
posButton = tk.Button(root, text="Set Autoclicking Position", command= startMouseListener)
posButton.pack(pady=10)

autoclickButton = tk.Button(root, text="Start Autoclicker", command= lambda: autoclick("left", float(intervalEntry.get())/1000, x_coord, y_coord))
autoclickButton.pack(pady=10)

root.mainloop()