
import tkinter as tk # import tkinter package
from time import sleep #import sleep
from servoControl import despenseSpice  # import continuous_servo from servoContro.py


# import screeninfo # import screeninfo package

root = tk.Tk() # create root widget ; main window


# settings of main window
root.title("Spice It Up!")
root.configure(background="#ffe599")
root.minsize(1280,720)
root.maxsize(1280,720)
root.geometry("1280x720")

# title text
tk.Label(root, text="Spice It Up!", font=('Noto Serif KR Black', 48, "underline"), fg="#3a2004", bg=root.cget("bg")).pack()

# dispense spice button function
is_dispensing = True
def button():
    global is_dispensing

    # determine if spice is dispensing or not
    if (is_dispensing):
        dispense_button.config(text="Stop dispensing", fg="#231200", bg="#d2b191")
        is_dispensing = False
    else:
        dispense_button.config(text="Start dispensing", fg="#3a2004", bg="#e0c3a7")
        is_dispensing = True
        despenseSpice(0)  # call continuous_servo function from servoContro.py


# dispense spice button
pixel = tk.PhotoImage(width=1, height=1)
dispense_button = tk.Button(root, text="Start dispensing", command = button, image=pixel, font=('Noto Serif KR Semibold', 36), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", height=124, width=459, compound="c")
dispense_button.pack(side="top", pady=100)





root.mainloop() # main event loop