#########################################################################################################
# DETAILS                                                                                               #
# - spiceItUpGUIv2.1                                                                                    #
# - based on figma sketch & spiceItUpGUIv1.1                                                            #
# - uses python's Tkinter library                                                                       #
# - meant for testing and integrating backend                                                           #
# - switches frames using GeeksForGeeks tutorial (light of this world)                                  #
#   - https://www.geeksforgeeks.org/python/tkinter-application-to-switch-between-different-page-frames/ #
#########################################################################################################


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
smallFont = ('VT323', 35)
fontColor = '#843b1b'
buttonColor = '#fadb8c'
pressedButton = '#eec04b'
pressedFont = '#692a0e'
winWidth = 1280
winHeight = 720


# class for initiallizing all GUI frames and defining show_frame function
class spiceItUpApp(tk.Tk):
	
    # __init__ function for class spiceItUpGUI
	def __init__(self, *args, **kwargs):
		
        # __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
        # set window size
		self.geometry(f"{winWidth}x{winHeight}")
		self.minsize(winWidth, winHeight)
		self.maxsize(winWidth, winHeight)
		
        # set window title
		self.title("Spice It Up!")
		
        # creating a container
		container = tk.Frame(self)
		container.pack(side='top', fill='both', expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
        # initiallizing frames to an empty array
		self.frames = {}
		
        # iterating through the page layouts
		for i in (startWin, dispenseSpiceWin, layoutWin, customMixesWin, selectDispenseWin, amountDispenseWin, selectLayoutWin):
			frame = i(container, self)
            # initiallizing frame
			self.frames[i] = frame
			frame.grid(row=0, column=0, sticky='nsew')
			
		self.showFrame(startWin)
	
    # display frame that is passed as a parameter
	def showFrame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
		

# class for start window
class startWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of start window
		self.configure(background=bgColor)
		# 4x2 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)

        # startWin title
		title = tk.Label(self, text="Spice It Up!", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=2, sticky=tk.N)

        # lilGuy dancing
		lilGuyDancing = AnimatedGif(self, './assets/lilGuy_dancing.gif', 0.5)
		lilGuyDancing.grid(row=1, column=0, rowspan=3)
		lilGuyDancing.start()

        # startWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
		dispenseButton = tk.Button(
			self, 
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
            command = lambda: controller.showFrame(dispenseSpiceWin)
        )
		dispenseButton.grid(row=1, column=1, sticky=tk.NW)
		
		mixesButton = tk.Button(
            self,
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
            command = lambda: controller.showFrame(customMixesWin)
        )
		mixesButton.grid(row=2, column=1, sticky=tk.NW)
		
		layoutButton = tk.Button(
            self,
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
            command = lambda: controller.showFrame(layoutWin)
        )
		layoutButton.grid(row=3, column=1, sticky=tk.NW)
		

# class for dispense spice window
class dispenseSpiceWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of dispense spice window
		self.configure(background=bgColor)
        # 4x2 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)

        # dispenseSpiceWin title
		title = tk.Label(self, text="Dispense Spice", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=2, sticky=tk.N)

        # lilGuy dancing
		lilGuyDancing = AnimatedGif(self, './assets/lilGuy_dancing.gif', 0.5)
		lilGuyDancing.grid(row=1, column=0, rowspan=3)
		lilGuyDancing.start()

        # dispenseSpiceWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
		singleButton = tk.Button(
			self, 
            text = "Single Spice", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 520,
            height = 120,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectDispenseWin)
        )
		singleButton.grid(row=1, column=1, sticky=tk.NW)
		
		mixButton = tk.Button(
            self,
            text= "Spice Mix",
            font = regularFont,
            fg = fontColor,
            bg = buttonColor,
            activeforeground = pressedFont,
            activebackground = pressedButton,
            width = 520,
            height = 120,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		mixButton.grid(row=2, column=1, sticky=tk.NW)
		
		backButton = tk.Button(
            self,
            text= "Back",
            font = regularFont,
            fg = fontColor,
            bg = buttonColor,
            activeforeground = pressedFont,
            activebackground = pressedButton,
            width = 520,
            height = 120,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		backButton.grid(row=3, column=1, sticky=tk.NW)


# class for layout window
class layoutWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of layout window
		self.configure(background=bgColor)
        # 4x7 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)
		self.columnconfigure(5, weight=1)
		self.columnconfigure(6, weight=1)

        # layoutWin title
		title = tk.Label(self, text="Spice Layout", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=7, sticky=tk.N)

        # layoutWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
        # button layout
		# |           |
		# | 0 1 2 3 4 |
		# | 5 6 7 8 9 |
		# |  confirm  |
		
		button0 = tk.Button(
			self, 
            text = "Spice 1", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button0.grid(row=1, column=1, sticky=tk.N)
		
		button1 = tk.Button(
			self, 
            text = "Spice 2", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button1.grid(row=1, column=2, sticky=tk.N)
		
		button2 = tk.Button(
			self, 
            text = "Spice 3", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button2.grid(row=1, column=3, sticky=tk.N)
		
		button3 = tk.Button(
			self, 
            text = "Spice 4", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button3.grid(row=1, column=4, sticky=tk.N)
		
		button4 = tk.Button(
			self, 
            text = "Spice 5", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button4.grid(row=1, column=5, sticky=tk.N)

		button5 = tk.Button(
			self, 
            text = "Spice 6", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button5.grid(row=2, column=1, sticky=tk.N)
		
		button6 = tk.Button(
			self, 
            text = "Spice 7", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button6.grid(row=2, column=2, sticky=tk.N)
		
		button7 = tk.Button(
			self, 
            text = "Spice 8", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button7.grid(row=2, column=3, sticky=tk.N)
		
		button8 = tk.Button(
			self, 
            text = "Spice 9", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button8.grid(row=2, column=4, sticky=tk.N)
		
		button9 = tk.Button(
			self, 
            text = "Spice 10", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectLayoutWin)
        )
		button9.grid(row=2, column=5, sticky=tk.N)
		
		confirm = tk.Button(
			self, 
            text = "Confirm", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		confirm.grid(row=3, column=2, columnspan=3, sticky=tk.N)


# class for custom mixes window
class customMixesWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of custom mixes window
		self.configure(background=bgColor)
        # 4x3 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

        # customMixesWin title
		title = tk.Label(self, text="Custom Spice Mixes", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=3, sticky=tk.N)

        # customMixesWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
		viewButton = tk.Button(
			self, 
            text = "View\nCustom Mixes", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 340,
            height = 340,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		viewButton.grid(row=1, rowspan=2, column=0, sticky=tk.N)
		
		addButton = tk.Button(
            self,
            text= "Add\nCustom Mix",
            font = regularFont,
            fg = fontColor,
            bg = buttonColor,
            activeforeground = pressedFont,
            activebackground = pressedButton,
            width = 340,
            height = 340,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		addButton.grid(row=1, rowspan=2, column=1, sticky=tk.N)
		
		removeButton = tk.Button(
            self,
            text= "Remove\nCustom Mix",
            font = regularFont,
            fg = fontColor,
            bg = buttonColor,
            activeforeground = pressedFont,
            activebackground = pressedButton,
            width = 340,
            height = 340,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		removeButton.grid(row=1, rowspan=2, column=2, sticky=tk.N)
		
		back = tk.Button(
            self,
            text= "Back",
            font = regularFont,
            fg = fontColor,
            bg = buttonColor,
            activeforeground = pressedFont,
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		back.grid(row=3, column=1, sticky=tk.N)


# class for spice selection window (dispense)
class selectDispenseWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of spice selection window
		self.configure(background=bgColor)
        # 4x7 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)
		self.columnconfigure(5, weight=1)
		self.columnconfigure(6, weight=1)

        # selectDispenseWin title
		title = tk.Label(self, text="Select Spice", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=7, sticky=tk.N)

        # layoutWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
        # button layout
		# |           |
		# | 0 1 2 3 4 |
		# | 5 6 7 8 9 |
		# |    back   |
		
		button0 = tk.Button(
			self, 
            text = "Spice 1", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button0.grid(row=1, column=1, sticky=tk.N)
		
		button1 = tk.Button(
			self, 
            text = "Spice 2", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button1.grid(row=1, column=2, sticky=tk.N)
		
		button2 = tk.Button(
			self, 
            text = "Spice 3", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button2.grid(row=1, column=3, sticky=tk.N)
		
		button3 = tk.Button(
			self, 
            text = "Spice 4", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button3.grid(row=1, column=4, sticky=tk.N)
		
		button4 = tk.Button(
			self, 
            text = "Spice 5", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button4.grid(row=1, column=5, sticky=tk.N)

		button5 = tk.Button(
			self, 
            text = "Spice 6", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button5.grid(row=2, column=1, sticky=tk.N)
		
		button6 = tk.Button(
			self, 
            text = "Spice 7", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button6.grid(row=2, column=2, sticky=tk.N)
		
		button7 = tk.Button(
			self, 
            text = "Spice 8", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button7.grid(row=2, column=3, sticky=tk.N)
		
		button8 = tk.Button(
			self, 
            text = "Spice 9", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button8.grid(row=2, column=4, sticky=tk.N)
		
		button9 = tk.Button(
			self, 
            text = "Spice 10", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(amountDispenseWin)
        )
		button9.grid(row=2, column=5, sticky=tk.N)
		
		back = tk.Button(
			self, 
            text = "Back", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(dispenseSpiceWin)
        )
		back.grid(row=3, column=2, columnspan=3, sticky=tk.N)
		

# class for select amount window (dispense)
class amountDispenseWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of select amount window
		self.configure(background=bgColor)
        # 4x3 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

        # amountDispenseWin title
		title = tk.Label(self, text="Select Amount", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=3, sticky=tk.N)

        # amountDispenseWin textbox
		amountBox = tk.Text(
			self,
			font = regularFont,
			fg = fontColor,
			bg = buttonColor,
			width = 10,
			height = 2
		)
		amountBox.grid(row=1, rowspan=1, column=1, columnspan=1, sticky=tk.N)

        # amountDispenseWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel

		gramsButton = tk.Button(
			self, 
            text = "Grams", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		gramsButton.grid(row=2, column=0, sticky=tk.N)
		
		teaspoonsButton = tk.Button(
            self,
            text= "Teaspoons",
            font = regularFont,
            fg = fontColor,
            bg = buttonColor,
            activeforeground = pressedFont,
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		teaspoonsButton.grid(row=2, column=1, sticky=tk.N)
		
		tablespoonsButton = tk.Button(
            self,
            text= "Tablespoons",
            font = regularFont,
            fg = fontColor,
            bg = buttonColor,
            activeforeground = pressedFont,
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(startWin)
        )
		tablespoonsButton.grid(row=2, column=2, sticky=tk.N)
		
		back = tk.Button(
            self,
            text= "Back",
            font = regularFont,
            fg = fontColor,
            bg = buttonColor,
            activeforeground = pressedFont,
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(selectDispenseWin)
        )
		back.grid(row=3, column=1, sticky=tk.N)


# class for spice selection window (layout)
class selectLayoutWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of spice selection window
		self.configure(background=bgColor)
        # 4x7 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)
		self.columnconfigure(5, weight=1)
		self.columnconfigure(6, weight=1)

        # selectDispenseWin title
		title = tk.Label(self, text="Select Spice", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=7, sticky=tk.N)

        # layoutWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
        # button layout
		# |           |
		# | 0 1 2 3 4 |
		# | 5 6 7 8 9 |
		# |    back   |
		
		button0 = tk.Button(
			self, 
            text = "Spice 1", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button0.grid(row=1, column=1, sticky=tk.N)
		
		button1 = tk.Button(
			self, 
            text = "Spice 2", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button1.grid(row=1, column=2, sticky=tk.N)
		
		button2 = tk.Button(
			self, 
            text = "Spice 3", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button2.grid(row=1, column=3, sticky=tk.N)
		
		button3 = tk.Button(
			self, 
            text = "Spice 4", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button3.grid(row=1, column=4, sticky=tk.N)
		
		button4 = tk.Button(
			self, 
            text = "Spice 5", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button4.grid(row=1, column=5, sticky=tk.N)

		button5 = tk.Button(
			self, 
            text = "Spice 6", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button5.grid(row=2, column=1, sticky=tk.N)
		
		button6 = tk.Button(
			self, 
            text = "Spice 7", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button6.grid(row=2, column=2, sticky=tk.N)
		
		button7 = tk.Button(
			self, 
            text = "Spice 8", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button7.grid(row=2, column=3, sticky=tk.N)
		
		button8 = tk.Button(
			self, 
            text = "Spice 9", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button8.grid(row=2, column=4, sticky=tk.N)
		
		button9 = tk.Button(
			self, 
            text = "Spice 10", 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		button9.grid(row=2, column=5, sticky=tk.N)
		
		back = tk.Button(
			self, 
            text = "Back", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(layoutWin)
        )
		back.grid(row=3, column=2, columnspan=3, sticky=tk.N)
		

# driver code
app = spiceItUpApp()
app.mainloop()