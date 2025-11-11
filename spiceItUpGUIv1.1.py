import tkinter as tk # import tkinter package
from time import sleep #import sleep

# create root widget ; main window
root = tk.Tk()

# settings of main window
root.title("Spice It Up!")
root.configure(background="#ffe599")
root.minsize(1280,658)
root.maxsize(1280,658)
root.geometry("1280x658")

# title text
rootTitle = tk.Label(root, text="Spice It Up!", font=('Noto Serif KR Black', 48, "underline"), fg="#3a2004", bg=root.cget("bg"))
rootTitle.grid(row=0, column=1, columnspan=3, pady=20, sticky="N")

############################################################################################

# dispense spice button function
def dispense(servoNum):
    print("Activating servo number {}".format(servoNum))

#    button layout
# |                |
# | 00 01 02 03 04 |
# | 10 11 12 13 14 |
# |                |
#
#   s0 s1 s2 s3 s4    <== servos


# dispense spice buttons
pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance

# top row
button00 = tk.Button(root, text="Spice 1", command=lambda: dispense(0), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button00.grid(row=3, column=0, padx=10, pady=10)

button01 = tk.Button(root, text="Spice 2", command=lambda: dispense(1), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button01.grid(row=3, column=1, padx=0, pady=10)

button02 = tk.Button(root, text="Spice 3", command=lambda: dispense(2), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button02.grid(row=3, column=2, padx=10, pady=10)

button03 = tk.Button(root, text="Spice 4", command=lambda: dispense(3), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button03.grid(row=3, column=3, padx=0, pady=10)

button04 = tk.Button(root, text="Spice 5", command=lambda: dispense(4), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button04.grid(row=3, column=4, padx=10, pady=10)

# bottom row
button10 = tk.Button(root, text="Spice 6", command=lambda: dispense(0), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button10.grid(row=4, column=0, padx=10)

button11 = tk.Button(root, text="Spice 7", command=lambda: dispense(1), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button11.grid(row=4, column=1, padx=0)

button12 = tk.Button(root, text="Spice 8", command=lambda: dispense(2), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button12.grid(row=4, column=2, padx=10)

button13 = tk.Button(root, text="Spice 9", command=lambda: dispense(3), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button13.grid(row=4, column=3, padx=0)

button14 = tk.Button(root, text="Spice 10", command=lambda: dispense(4), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button14.grid(row=4, column=4, padx=10)

############################################################################################

# main event loop
root.mainloop()
