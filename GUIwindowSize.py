import tkinter as tk # import tkinter package

root = tk.Tk() # create root widget ; main window


# settings of main window
root.title("Spice It Up!")
root.configure(background="#ffe599")
root.geometry("1280x720")


# display main window size
def updateSize():
    rootWidth = str(root.winfo_width())
    rootHeight = str(root.winfo_height())
    windowSizeLabel.config(text="Width: " + rootWidth + ", Height:" + rootHeight) # update label text
    root.after(100, updateSize) # update every 100ms

# define label
windowSizeLabel = tk.Label(root, text = "", font=('Noto Serif KR Black', 36), fg="#3a2004", bg=root.cget("bg") )
windowSizeLabel.pack(side="top")

updateSize()

root.mainloop() # main event loop

