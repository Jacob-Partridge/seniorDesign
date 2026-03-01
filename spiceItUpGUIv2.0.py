#####################################################
# DETAILS                                           #
# - spiceItUpGUIv2.0                                #
# - based on figma sketch & spiceItUpGUIv1.1        #
# - uses python's Tkinter library                   #
# - meant for testing and integrating backend       #
#####################################################


import tkinter as tk # import tkinter package
from time import sleep # import sleep function

# settings for visuals
bgColor = '#f6efeb'
titleFont = ('VT323', 96)
regularFont = ('VT323', 48)
fontColor = '#843b1b'
buttonColor = '#fadb8c'
pressedButton = '#eec04b'
pressedFont = '#692a0e'
winWidth = 1280
winHeight = 720

# create start window
startWin = tk.Tk()

# settings of start window
startWin.title("Starting Screen")
startWin.configure(background=bgColor)
startWin.minsize(winWidth, winHeight)
startWin.maxsize(winWidth, winHeight)
# 4x2 grid
startWin.rowconfigure(0, weight=1)
startWin.rowconfigure(1, weight=1)
startWin.rowconfigure(2, weight=1)
startWin.rowconfigure(3, weight=1)
startWin.columnconfigure(0, weight=1)
startWin.columnconfigure(1, weight=1)

# startWin title
startWinTitle = tk.Label(startWin, text="Spice It Up!", font=titleFont, fg=fontColor, bg=bgColor)
startWinTitle.grid(row=0, column=0, columnspan=2, sticky=tk.N)

# lilGuy image
lilGuyStanding = tk.PhotoImage(file='./assets/lilGuy_standing.png')
lilGuyImage = tk.Label(startWin, image=lilGuyStanding)
lilGuyImage.grid(row=1, column=0, rowspan=3)

# startWin buttons
pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
dispenseButton = tk.Button(
    startWin, 
    text = "Dispense Spices", 
    font = regularFont, 
    fg = fontColor, 
    bg = buttonColor, 
    activeforeground = pressedFont, 
    activebackground = pressedButton,
    width = 520,
    height = 120,
    image = pixel,
    compound = tk.CENTER,
    command = lambda: goDispenseWin()
)
dispenseButton.grid(row=1, column=1, sticky=tk.NW)
mixesButton = tk.Button(
    startWin,
    text= "Custom Spice Mixes",
    font = regularFont,
    fg = fontColor,
    bg = buttonColor,
    activeforeground = pressedFont,
    activebackground = pressedButton,
    width = 520,
    height = 120,
    image = pixel,
    compound = tk.CENTER,
    command = lambda: goMixesWin()
)
mixesButton.grid(row=2, column=1, sticky=tk.NW)
layoutButton = tk.Button(
    startWin,
    text= "Change Layout",
    font = regularFont,
    fg = fontColor,
    bg = buttonColor,
    activeforeground = pressedFont,
    activebackground = pressedButton,
    width = 520,
    height = 120,
    image = pixel,
    compound = tk.CENTER,
    command = lambda: goLayoutWin()
)
layoutButton.grid(row=3, column=1, sticky=tk.NW)

# function for dispenseButton
def goDispenseWin():
    # hide startWin
    startWin.withdraw()
    startWin.deiconify()

# function for mixesButton
def goMixesWin():
    # hide startWin
    startWin.withdraw()
    startWin.deiconify()

# function for layoutButton
def goLayoutWin():
    # hide startWin
    startWin.withdraw()
    startWin.deiconify()




# start window event loop
startWin.mainloop()