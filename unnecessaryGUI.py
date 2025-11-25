import tkinter as tk # import tkinter package
from time import sleep # import sleep
# from servoControl import turnServo

# create root widget ; main window
root = tk.Tk()

# settings of main window
root.title("Spice It Up!")
root.configure(background="#ffe599")

pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance

# title text
rootTitle = tk.Label(root, text="Spice It Up!", font=('Noto Serif KR Black', 48, "underline"), fg="#3a2004", bg=root.cget("bg"))
rootTitle.grid(row=0, column=1, columnspan=3, pady=20, sticky="N")

button00 = tk.Button(root, text="Servo 1", command=lambda: dispense(0), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button00.grid(row=3, column=0, padx=10, pady=10)

button01 = tk.Button(root, text="Servo 2", command=lambda: dispense(1), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button01.grid(row=3, column=1, padx=0, pady=10)

button02 = tk.Button(root, text="Servo 3", command=lambda: dispense(2), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button02.grid(row=3, column=2, padx=10, pady=10)

button03 = tk.Button(root, text="Servo 4", command=lambda: dispense(3), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button03.grid(row=3, column=3, padx=0, pady=10)

button04 = tk.Button(root, text="Servo 5", command=lambda: dispense(4), image=pixel, font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", activeforeground="#231200", activebackground="#d2b191", width = 236, compound="c")
button04.grid(row=3, column=4, padx=10, pady=10)

############################################################################################

# Function to return from the control window to the main GUI
def go_back(new_window):
    # 1. Destroy the current secondary window
    new_window.destroy()
    # 2. Show the main window again
    root.deiconify() 
    print("Returned to main GUI.")

# dispense spice button function (Now opens the control window)
def dispense(servoNum):
    print(f"Opening control for Servo {servoNum + 1}")
    
    # 1. Hide the main window
    root.withdraw() 
    
    # 2. Create the new Toplevel window for control
    control_window = tk.Toplevel(root)
    control_window.title(f"Control Panel for Servo {servoNum + 1}")
    control_window.geometry("500x250")
    control_window.configure(background="#ffe599")
    
    # Optional: Handle window closing (X button) to return to main GUI
    control_window.protocol("WM_DELETE_WINDOW", lambda: go_back(control_window))

    # Frame to hold buttons for layout
    button_frame = tk.Frame(control_window, bg=control_window.cget("bg"))
    button_frame.pack(expand=True, fill='both', pady=20)

    # --- Create the three control buttons ---
    
    # Left Button
    left_button = tk.Button(
        button_frame, 
        text="Left", 
        command=lambda: turnServo(servoNum, "LEFT"),
        font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", 
        activeforeground="#231200", activebackground="#d2b191", 
        width=10
    )
    left_button.pack(side='left', padx=15, pady=20)

    # Right Button
    right_button = tk.Button(
        button_frame, 
        text="Right", 
        command=lambda: turnServo(servoNum, "RIGHT"),
        font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#e0c3a7", 
        activeforeground="#231200", activebackground="#d2b191", 
        width=10
    )
    right_button.pack(side='left', padx=15, pady=20)
    
    # Back Button
    # Note: We pass the control_window object to the go_back function
    back_button = tk.Button(
        button_frame, 
        text="Back", 
        command=lambda: go_back(control_window), 
        font=('Noto Serif KR Semibold', 24), fg="#3a2004", bg="#b4c7dc", # Different color for emphasis
        activeforeground="#231200", activebackground="#9fb1c7", 
        width=10
    )
    back_button.pack(side='left', padx=15, pady=20)


if __name__ == '__main__':
    root.mainloop()