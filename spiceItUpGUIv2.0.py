#####################################################
# DETAILS                                           #
# - spiceItUpGUIv2.0                                #
# - based on figma sketch & spiceItUpGUIv1.1        #
# - uses python's Tkinter library                   #
# - starting frame only						      	#
#####################################################


import tkinter as tk # import tkinter package
import sys
import time

# class for animated GIFs
# credit to: https://github.com/olesk75/AnimatedGIF  (saved my life)
class AnimatedGif(tk.Label):
	def __init__(self, root, gif_file, delay=0.04):
		# paramaters
		# :param root: tk.parent
		# :param gif_file: filename (and path) of animated gif
		# :param delay: delay between frames in the gif animation (float)
		
		tk.Label.__init__(self, root)
		self.root = root
		self.gif_file = gif_file
		self.delay = delay  # animation delay in seconds
		self.stop = False  # thread exit request flag

		self._num = 0

	def start(self):
		# starts non-threaded version that we need to manually update()
		self.start_time = time.time()  # starting timer
		self._animate()

	def stop(self):
		# this stops the after loop that runs the animation, if we are using the after() approach
		self.stop = True

	def _animate(self):
		try:
			self.gif = tk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))  # looping through the frames
			self.configure(image=self.gif)
			self._num += 1
		except tk.TclError:  # when we try a frame that doesn't exist, we know we have to start over from zero
			self._num = 0
			# loop through frames again to avoid pause
			self.gif = tk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))
			self.configure(image=self.gif)
			self._num += 1
		if not self.stop:    # if the stop flag is set, don't repeat
			self.root.after(int(self.delay*1000), self._animate)

	def start_thread(self):
		# this starts the thread that runs the animation, if we are using a threaded approach
		from threading import Thread  # only import the module if we need it
		self._animation_thread = Thread()
		self._animation_thread = Thread(target=self._animate_thread).start()  # forks a thread for the animation

	def stop_thread(self):
		# this stops the thread that runs the animation, if we are using a threaded approach
		self.stop = True

	def _animate_thread(self):
		# updates animation, if it is running as a separate thread
		while self.stop is False:  # normally this would block mainloop(), but not here, as this runs in separate thread
			try:
				time.sleep(self.delay)
				self.gif = tk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))  # looping through the frames
				self.configure(image=self.gif)
				self._num += 1
			except tk.TclError:  # when we try a frame that doesn't exist, we know we have to start over from zero
				self._num = 0
			except RuntimeError:
				sys.exit()


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


# lilGuy dancing
lilGuyDancing = AnimatedGif(startWin, './assets/lilGuy_dancing.gif', 0.5)
lilGuyDancing.grid(row=1, column=0, rowspan=3)
lilGuyDancing.start()

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


if __name__ == '__main__':
    # start window event loop
    startWin.mainloop()
