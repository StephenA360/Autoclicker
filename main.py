#Package imports
import pyautogui
from pynput import keyboard
from pynput import mouse
import tkinter as tk
import threading

pyautogui.PAUSE = 0 #Removes the 0.1s interval limit on pyautogui

#Global variables
end = keyboard.Key.esc
check = False
x_coord = 0
y_coord = 0
mouseThread = None

#Functions for ending the autoclicker by the hotkey (esc)
def endPress(key, injected):
    global check
    if key == end:
        check = True
        return False

def endPressListener():
    with keyboard.Listener(on_press=endPress) as listener:
        listener.join()

#Main autoclick function
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

#Functions for finding the autoclicking position
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

#Function that handles the threading of finding the autoclicking position
def startMouseListener():
    global mouseThread
    if mouseThread is None or not mouseThread.is_alive():
        mouseThread = threading.Thread(target=mousePosListener)
        mouseThread.daemon = True
        mouseThread.start()
    else:
        print("Mouse thread is already running.")

#Function to dynamically change the CPS label when changing the interval entry element
def entryChanged(*args):
    try:
        cpsStringVar.set(str(1000/int(intervalEntry.get())) + " CPS")
    except ValueError:
        cpsStringVar.set("Invalid input")
    
#GUI (Tkinter)
root = tk.Tk()
root.title("Autoclicker Menu")
root.geometry("400x450")

titleLabel = tk.Label(root, text="Autoclicker", font=("Helvetica", 12, "bold"))
titleLabel.pack(pady=20)

endStringVar = tk.StringVar()
endStringVar.set(f"End Key: {end}")
endKeyLabel = tk.Label(root, textvariable=endStringVar)
endKeyLabel.pack(pady=20)

intervalLabel = tk.Label(root, text="Enter the interval between clicks in milliseconds (minimum of 5-10 ms)")
intervalLabel.pack(pady=10)
intervalStringVar = tk.StringVar()
intervalStringVar.set("100")
intervalStringVar.trace_add("write", entryChanged)
intervalEntry = tk.Entry(root, textvariable=intervalStringVar)
intervalEntry.pack(pady=20)

cpsStringVar = tk.StringVar()
cpsStringVar.set(str(1000/int(intervalEntry.get())) + " CPS")
cpsLabel = tk.Label(root, textvariable=cpsStringVar)
cpsLabel.pack(pady=20)

pos = tk.StringVar()
pos.set(f"Autoclicking Position: ({x_coord}, {y_coord})")
posLabel = tk.Label(root, textvariable = pos)
posLabel.pack(pady=10)
posButton = tk.Button(root, text="Set Autoclicking Position", command= startMouseListener)
posButton.pack(pady=10)

autoclickButton = tk.Button(root, text="Start Autoclicker", command= lambda: autoclick("left", float(intervalEntry.get())/1000, x_coord, y_coord))
autoclickButton.pack(pady=10)

root.mainloop()