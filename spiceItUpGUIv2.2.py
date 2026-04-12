#########################################################################################################
# DETAILS                                                                                               #
# - spiceItUpGUIv2.2                                                                                   #
# - based on figma sketch & spiceItUpGUIv2.1                                                            #
# - uses python's Tkinter library                                                                       #
# - meant for testing and integrating backend                                                           #
# - switches frames using GeeksForGeeks tutorial (light of this world)                                  #
#   - https://www.geeksforgeeks.org/python/tkinter-application-to-switch-between-different-page-frames/ #
#########################################################################################################

import sys
import time # import time class
import tkinter as tk # import tkinter package
import backEnd # import backend class
from threading import Thread # import threading classes for backend and GUI to run simultaneously

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
			self.configure(image=self.gif, borderwidth=0, highlightthickness=0)
			self._num += 1
		except tk.TclError:  # when we try a frame that doesn't exist, we know we have to start over from zero
			self._num = 0
			# loop through frames again to avoid pause
			self.gif = tk.PhotoImage(file=self.gif_file, format='gif -index {}'.format(self._num))
			self.configure(image=self.gif, borderwidth=0, highlightthickness=0)
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

# class for animated text		
class AnimatedTxt(tk.Label):
	def __init__(self, root, texts, delay=0.04):
		# paramaters
		# :param root: tk.parent
		# :param texts: array of texts to loop through
		# :param delay: delay between frames (float)
		
		tk.Label.__init__(self, root)
		self.root = root
		self.text_array = texts
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
			self.configure(text=self.text_array[self._num], font=titleFont, fg=fontColor, bg=bgColor)
			if self._num < len(self.text_array) - 1:
				self._num += 1
			else:
				self._num = 0
		except tk.TclError:  # when we try a frame that doesn't exist, we know we have to start over from zero
			self._num = 0
			# loop through frames again to avoid pause
			self.configure(text=self.text_array[self._num], font=titleFont, fg=fontColor, bg=bgColor)
			self._num += 1
		if not self.stop:    # if the stop flag is set, don't repeat
			self.root.after(int(self.delay*1000), self._animate)
			
# class for scrollable canvas frame
# credit to https://stackoverflow.com/questions/20645532 and https://stackoverflow.com/questions/66213754 (my guiding stars)
class ScrollableFrame(tk.Frame):
    """
    There is no way to scroll <tkinter.Frame> so we are
    going to create a canvas and place the frame there.
    Scrolling the canvas will give the illusion of scrolling
    the frame
    Partly taken from:
        https://blog.tecladocode.com/tkinter-scrollable-frames/
        https://stackoverflow.com/a/17457843/11106801
    master_frame---------------------------------------------------------
    | dummy_canvas-----------------------------------------  y_scroll--  |
    | | self---------------------------------------------  | |         | |
    | | |                                                | | |         | |
    | | |                                                | | |         | |
    | | |                                                | | |         | |
    | |  ------------------------------------------------  | |         | |
    |  ----------------------------------------------------   ---------  |
    | x_scroll---------------------------------------------              |
    | |                                                    |             |
    |  ----------------------------------------------------              |
     --------------------------------------------------------------------
    """
    def __init__(self, master=None, scroll_speed:int=2, hscroll:bool=False,
                 vscroll:bool=True, bd:int=0, scrollbar_kwargs={},
                 bg="#f0f0ed", **kwargs):
        assert isinstance(scroll_speed, int), "`scroll_speed` must be an int"
        self.scroll_speed = scroll_speed

        self.master_frame = tk.Frame(master, bd=bd, bg=bg)
        self.master_frame.grid_rowconfigure(0, weight=1)
        self.master_frame.grid_columnconfigure(0, weight=1)
        self.dummy_canvas = tk.Canvas(self.master_frame, highlightthickness=0,
                                      bd=0, bg=bg, **kwargs)
        super().__init__(self.dummy_canvas, bg=bg)

        # Create the 2 scrollbars
        if vscroll:
            self.v_scrollbar = tk.Scrollbar(self.master_frame,
                                            orient="vertical",
                                            command=self.dummy_canvas.yview,
                                            **scrollbar_kwargs)
            self.v_scrollbar.grid(row=0, column=1, sticky="news")
            self.dummy_canvas.configure(yscrollcommand=self.v_scrollbar.set)
        if hscroll:
            self.h_scrollbar = tk.Scrollbar(self.master_frame,
                                            orient="horizontal",
                                            command=self.dummy_canvas.xview,
                                            **scrollbar_kwargs)
            self.h_scrollbar.grid(row=1, column=0, sticky="news")
            self.dummy_canvas.configure(xscrollcommand=self.h_scrollbar.set)

        # Place `self` inside `dummy_canvas`
        self.window_id = self.dummy_canvas.create_window((0, 0), window=self, anchor="nw")
        self.dummy_canvas.bind("<Configure>", self._on_canvas_resize)
        # Place `dummy_canvas` inside `master_frame`
        self.dummy_canvas.grid(row=0, column=0, sticky="news")
		
        # Update scroll region
        self.bind("<Configure>", self.scrollbar_scrolling, add=True)

        # Geometry methods
        self.pack = self.master_frame.pack
        self.grid = self.master_frame.grid
        self.place = self.master_frame.place
        self.pack_forget = self.master_frame.pack_forget
        self.grid_forget = self.master_frame.grid_forget
        self.place_forget = self.master_frame.place_forget
		
        # Bind dragging to canvas itself
        self._bind_widget(self.dummy_canvas)

    def scroll_start(self, event):
        if not self._canvas_alive():
            return
        self.dummy_canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        if not self._canvas_alive():
            return
        self.dummy_canvas.scan_dragto(event.x, event.y, gain=1)
		
    def _canvas_alive(self):
        return hasattr(self, "dummy_canvas") and self.dummy_canvas and self.dummy_canvas.winfo_exists()

    def _bind_widget(self, widget):
		# Bind drag events to a widget
        widget.bind("<ButtonPress-1>", self.scroll_start)
        widget.bind("<B1-Motion>", self.scroll_move)
		
    def _on_canvas_resize(self, event):
        if not self._canvas_alive():
            return

        bbox = self.dummy_canvas.bbox("all")
        if not bbox:
            return

        content_width = bbox[2]
        canvas_width = event.width

        # Only stretch if content is smaller than canvas
        if content_width < canvas_width:
            self.dummy_canvas.itemconfig(self.window_id, width=canvas_width)
        else:
            self.dummy_canvas.itemconfig(self.window_id, width=content_width)

    # Bind all children recursively
	# Call AFTER adding widgets
    def bind_children(self, widget=None):
        if widget is None:
            widget = self
			
        self._bind_widget(widget)
        for child in widget.winfo_children():
            self.bind_children(child)

    def scrollbar_scrolling(self, event=None):
        if not self._canvas_alive():
            return
        region = list(self.dummy_canvas.bbox("all"))
        if region:
            region[2] = max(self.dummy_canvas.winfo_width(), region[2])
            region[3] = max(self.dummy_canvas.winfo_height(), region[3])
            self.dummy_canvas.configure(scrollregion=region)

    def resize(self, fit:str=None, height:int=None, width:int=None) -> None:
        """
        Resizes the frame to fit the widgets inside. You must either
        specify (the `fit`) or (the `height` or/and the `width`) parameter.
        Parameters:
            fit:str       `fit` can be either `FIT_WIDTH` or `FIT_HEIGHT`.
                          `FIT_WIDTH` makes sure that the frame's width can
                           fit all of the widgets. `FIT_HEIGHT` is simmilar
            height:int     specifies the height of the frame in pixels
            width:int      specifies the width of the frame in pixels
        To do:
            ALWAYS_FIT_WIDTH
            ALWAYS_FIT_HEIGHT
        """
        if height is not None:
            self.dummy_canvas.config(height=height)
        if width is not None:
            self.dummy_canvas.config(width=width)
        if fit == "fit_width":
            super().update()
            self.dummy_canvas.config(width=super().winfo_width())
        elif fit == "fit_height":
            super().update()
            self.dummy_canvas.config(height=super().winfo_height())
        else:
            raise ValueError("Unknown value for the `fit` parameter.")
    fit = resize

    def destroy(self):
        try:
			# Unbind from canvas
            self.dummy_canvas.unbind("<ButtonPress-1>")
            self.dummy_canvas.unbind("<B1-Motion>")
        except:
            pass
			
        self.dummy_canvas = None
        super().destroy()
		

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


# global array for layout spice names
spices = ["Empty", "Salt", "Black\nPepper", "Garlic\nPowder", "Onion\nPowder", "Paprika", "Cumin", "Chili\nPowder", "Ground\nGinger", "Dried\nOregeno", "Brown\nSugar"]
# global array for current spice layout
currentLayout = ["Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty", "Empty"]
# functions for changing layout buttons
def changeLayoutIndex(index):
	global changingLayout # global variable for index of currentLayout that is being changed
	changingLayout = index
def changeLayoutLabel(spice):
    currentLayout[changingLayout] = spice
	
def startSingleThread(target, args):
    global dispenseThread
    dispenseThread = Thread(target=target, args=args)
    dispenseThread.start()

# created backend object to call backend functions from GUI
backend = backEnd.SpiceItUpBackend()

backend.getRecipes() # testing getRecipes function in backend

# global variable to store spice selection for dispensing
spice = ''

# Global variables to track when dispensing thread is complete


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
		
		self.frames_container = container
		self.current_frame = None
			
		self.showFrame(startWin)
	
    # display frame that is passed as a parameter
	def showFrame(self, cont):
		# destroy current frame (if it exists)
		if self.current_frame is not None:
			self.current_frame.destroy()
			
        # create the new frame
		frame = cont(self.frames_container, self)
		
        # store and display the new frame
		self.current_frame = frame
		frame.grid(row=0, column=0, sticky=tk.NSEW)
		

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
		lilGuyDancing.grid(row=1, column=0, rowspan=3, columnspan=1)
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
		lilGuyDancing.grid(row=1, column=0, rowspan=3, columnspan=1)
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
            command = lambda: controller.showFrame(selectMixDispenseWin)
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
		title = tk.Label(self, text="Current Layout", font=titleFont, fg=fontColor, bg=bgColor)
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
            text = currentLayout[0], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
                changeLayoutIndex(0)
            )
        )
		button0.grid(row=1, column=1, sticky=tk.N)
		
		button1 = tk.Button(
			self, 
            text = currentLayout[1], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(1)
            )
        )
		button1.grid(row=1, column=2, sticky=tk.N)
		
		button2 = tk.Button(
			self, 
            text = currentLayout[2], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(2)
            )
        )
		button2.grid(row=1, column=3, sticky=tk.N)
		
		button3 = tk.Button(
			self, 
            text = currentLayout[3], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(3)
            )
        )
		button3.grid(row=1, column=4, sticky=tk.N)
		
		button4 = tk.Button(
			self, 
            text = currentLayout[4], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(4)
            )
        )
		button4.grid(row=1, column=5, sticky=tk.N)

		button5 = tk.Button(
			self, 
            text = currentLayout[5], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(5)
            )
        )
		button5.grid(row=2, column=1, sticky=tk.N)
		
		button6 = tk.Button(
			self, 
            text = currentLayout[6], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(6)
            )
        )
		button6.grid(row=2, column=2, sticky=tk.N)
		
		button7 = tk.Button(
			self, 
            text = currentLayout[7], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(7)
            )
        )
		button7.grid(row=2, column=3, sticky=tk.N)
		
		button8 = tk.Button(
			self, 
            text = currentLayout[8], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(8)
            )
        )
		button8.grid(row=2, column=4, sticky=tk.N)
		
		button9 = tk.Button(
			self, 
            text = currentLayout[9], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: (
				controller.showFrame(selectLayoutWin),
				changeLayoutIndex(9)
            )
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
            command = lambda: [backend.changeSpiceLayouts(currentLayout), 
							   controller.showFrame(startWin)]
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
            command = lambda: controller.showFrame(viewCustomWin)
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
            command = lambda: controller.showFrame(addCustomDetailsWin)
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
            command = lambda: controller.showFrame(deleteCustomWin)
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


# class for spice selection window (dispense single)
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
            text = currentLayout[0], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[0])]
        )
		button0.grid(row=1, column=1, sticky=tk.N)
		
		button1 = tk.Button(
			self, 
            text = currentLayout[1], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[1])]
        )
		button1.grid(row=1, column=2, sticky=tk.N)
		
		button2 = tk.Button(
			self, 
            text = currentLayout[2], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[2])]
        )
		button2.grid(row=1, column=3, sticky=tk.N)
		
		button3 = tk.Button(
			self, 
            text = currentLayout[3], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[3])]
        )
		button3.grid(row=1, column=4, sticky=tk.N)
		
		button4 = tk.Button(
			self, 
            text = currentLayout[4], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[4])]
        )
		button4.grid(row=1, column=5, sticky=tk.N)

		button5 = tk.Button(
			self, 
            text = currentLayout[5], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[5])]
        )
		button5.grid(row=2, column=1, sticky=tk.N)
		
		button6 = tk.Button(
			self, 
            text = currentLayout[6], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
			
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[6])]
        )
		button6.grid(row=2, column=2, sticky=tk.N)
		
		button7 = tk.Button(
			self, 
            text = currentLayout[7], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[7])]
        )
		button7.grid(row=2, column=3, sticky=tk.N)
		
		button8 = tk.Button(
			self, 
            text = currentLayout[8], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[8])]
        )
		button8.grid(row=2, column=4, sticky=tk.N)
		
		button9 = tk.Button(
			self, 
            text = currentLayout[9], 
            font = smallFont,
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: [controller.showFrame(amountDispenseWin),
							   globals().update(spice=currentLayout[9])]
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
		

# class for select amount window (dispense single)
class amountDispenseWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of select amount window
		self.configure(background=bgColor)
        # 4x5 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)

        # amountDispenseWin title
		title = tk.Label(self, text="Select Amount", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=5, sticky=tk.N)

        # amountDispenseWin textbox
		self.amountBox = tk.Label(
			self,
			font = regularFont,
			fg = fontColor,
			bg = buttonColor,
			width = 10,
			text="0"
		)
		self.amountBox.grid(row=1, rowspan=1, column=2, columnspan=1, sticky=tk.N)

        # amountDispenseWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel

		plusOneButton = tk.Button(
			self, 
            text = "+1", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), 1)))
        )
		plusOneButton.grid(row=1, rowspan=1, column=3, columnspan=1, sticky=tk.NE, padx=10)
		
		plusFiveButton = tk.Button(
			self, 
            text = "+5", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), 5)))
        )
		plusFiveButton.grid(row=1, rowspan=1, column=4, columnspan=1, sticky=tk.NW)
		
		minusOneButton = tk.Button(
			self, 
            text = "-1", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), -1)))
        )
		minusOneButton.grid(row=1, rowspan=1, column=1, columnspan=1, sticky=tk.NW, padx=10)
		
		minusFiveButton = tk.Button(
			self, 
            text = "-5", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), -5)))
        )
		minusFiveButton.grid(row=1, rowspan=1, column=0, columnspan=1, sticky=tk.NE)
		
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
            command = lambda: [Thread(target=backend.despenseSpice, args=(spice, self.amountBox.cget("text"),
																		  gramsButton['text'])).start(),
								controller.showFrame(waitingWin)]
        )
		gramsButton.grid(row=2, column=0, columnspan=2, sticky=tk.N)
		
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
            command = lambda: [startSingleThread(backend.despenseSpice, (spice, self.amountBox.cget("text"), teaspoonsButton['text'])),
							   time.sleep(.5),
							   controller.showFrame(waitingWin)]
					   
        )
		teaspoonsButton.grid(row=2, column=2, sticky=tk.N)
		
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
            command = lambda: [startSingleThread(backend.despenseSpice, (spice, self.amountBox.cget("text"), tablespoonsButton['text'])),
							   time.sleep(.5),
							   controller.showFrame(waitingWin)]
        )
		tablespoonsButton.grid(row=2, column=3, columnspan=2, sticky=tk.N)
		
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
		back.grid(row=3, column=2, sticky=tk.N)


# class for spice selection window (layout) (scrollable buttons)
class selectLayoutWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x3 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

        # selectLayoutWin title
		title = tk.Label(self, text="Select Spice", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=3, sticky=tk.N)

        # scrollable frame for scrollable buttons
		frame = ScrollableFrame(self, width=1280, height=400, hscroll=False, vscroll=False, bg=bgColor)
		frame.grid(row=1, rowspan=2, column=0, columnspan=3, sticky=tk.S)


        # selectLayoutWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
		for spice in spices:
			button = tk.Button(
				frame,
				text = spice,
				font = smallFont,
				fg = fontColor,
				bg = buttonColor,
				activeforeground = pressedFont,
				activebackground = pressedButton,
				width = 340,
				height = 340,
				image = pixel,
				compound = tk.CENTER,
				command = lambda spice=spice: (
					changeLayoutLabel(spice),
					controller.showFrame(layoutWin)
                )
            )
			button.grid(row=0, column=spices.index(spice), padx=10)
			

		frame.bind_children()
		frame.resize("fit_height")

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
		back.grid(row=3, column=1, columnspan=1)


# class for waiting window
class waitingWin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # settings of window
        self.configure(background=bgColor)
        # 4x5 grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        # waiting text
        dispensingTxts = ["Dispensing.", " Dispensing..", "  Dispensing..."]
        dispensingTxt = AnimatedTxt(self, dispensingTxts, 1)
        dispensingTxt.grid(row=1, column=1, columnspan=3, sticky=tk.S)
        dispensingTxt.start()
        plsWaitTxt = tk.Label(self, text=" Please Wait :) ", font=titleFont, fg=fontColor, bg=bgColor)
        plsWaitTxt.grid(row=2, column=1, columnspan=3, sticky=tk.N)

        self.checkThread(controller)
        # switch to finishedWin when done dispensing

    def checkThread(self, controller):
        if not dispenseThread.is_alive():
            controller.showFrame(finishedWin)
        else:
            controller.after(100, lambda: self.checkThread(controller))

# class for finished window
class finishedWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x5 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)

        # finished text
		finishedTxt = tk.Label(self, text="Finished Dispensing!", font=titleFont, fg=fontColor, bg=bgColor)
		finishedTxt.grid(row=1, column=1, columnspan=3, sticky=tk.S)

		enjoyTxt = tk.Label(self, text="Enjoy!", font=titleFont, fg=fontColor, bg=bgColor)
		enjoyTxt.grid(row=2, column=1, columnspan=3, sticky=tk.N)

        # finished GIF
		# TO BE ADDED
		
        # switch back to startWin
		controller.after(3000, lambda: controller.showFrame(startWin))


# class for spice mix selection window (dispense mix)
# WIP
# NEED TO FIX BUTTON LABELS
class selectMixDispenseWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x3 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

        # selectMixDispenseWin title
		title = tk.Label(self, text="Select Spice Mix", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=3, sticky=tk.N)

        # scrollable frame for scrollable buttons
		frame = ScrollableFrame(self, width=1280, height=400, hscroll=False, vscroll=False, bg=bgColor)
		frame.grid(row=1, rowspan=2, column=0, columnspan=3, sticky=tk.S)


        # selectMixDispenseWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel

		for spice in spices:
			button = tk.Button(
				frame,
				text = spice,
				font = smallFont,
				fg = fontColor,
				bg = buttonColor,
				activeforeground = pressedFont,
				activebackground = pressedButton,
				width = 340,
				height = 340,
				image = pixel,
				compound = tk.CENTER,
				command = lambda spice=spice: (
					controller.showFrame(amountMixDispenseWin)
                )
            )
			button.grid(row=0, column=spices.index(spice), padx=10)
			

		frame.bind_children()
		frame.resize("fit_height")

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
		back.grid(row=3, column=1, columnspan=1)


# class for select amount window (dispense mix)
class amountMixDispenseWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of select amount window
		self.configure(background=bgColor)
        # 4x5 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)

        # amountDispenseWin title
		title = tk.Label(self, text="Select Amount", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=5, sticky=tk.N)

        # amountDispenseWin textbox
		self.amountBox = tk.Label(
			self,
			font = regularFont,
			fg = fontColor,
			bg = buttonColor,
			width = 10,
			text="0"
		)
		self.amountBox.grid(row=1, rowspan=1, column=2, columnspan=1, sticky=tk.N)

        # amountDispenseWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel

		plusOneButton = tk.Button(
			self, 
            text = "+1", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), 1)))
        )
		plusOneButton.grid(row=1, rowspan=1, column=3, columnspan=1, sticky=tk.NE, padx=10)
		
		plusFiveButton = tk.Button(
			self, 
            text = "+5", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: backend.updateAmountGUI(int(self.amountBox.cget("text")), 5)
        )
		plusFiveButton.grid(row=1, rowspan=1, column=4, columnspan=1, sticky=tk.NW)
		
		minusOneButton = tk.Button(
			self, 
            text = "-1", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: backend.updateAmountGUI(int(self.amountBox.cget("text")), -1)
        )
		minusOneButton.grid(row=1, rowspan=1, column=1, columnspan=1, sticky=tk.NW, padx=10)
		
		minusFiveButton = tk.Button(
			self, 
            text = "-5", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: backend.updateAmountGUI(int(self.amountBox.cget("text")), -5)
        )
		minusFiveButton.grid(row=1, rowspan=1, column=0, columnspan=1, sticky=tk.NE)
		
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
            command = lambda: [controller.showFrame(waitingWin),
                               backend.despenseSpice(spice, self.amountBox.cget("text"),
													 gramsButton['text'])]
        )
		gramsButton.grid(row=2, column=0, columnspan=2, sticky=tk.N)
		
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
            command = lambda: [controller.showFrame(waitingWin),
							   backend.despenseSpice(spice, self.amountBox.cget("text"),
							                         teaspoonsButton['text'])]
        )
		teaspoonsButton.grid(row=2, column=2, sticky=tk.N)
		
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
            command = lambda: [controller.showFrame(waitingWin),
							   backend.despenseSpice(spice, self.amountBox.cget("text"),
							                         tablespoonsButton['text'])]
        )
		tablespoonsButton.grid(row=2, column=3, columnspan=2, sticky=tk.N)
		
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
            command = lambda: controller.showFrame(selectMixDispenseWin)
        )
		back.grid(row=3, column=2, sticky=tk.N)


# class for view custom mixes window (view)
# WIP
# NEED TO FIX BUTTON LABELS
class viewCustomWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x3 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

        # viewCustomWin title
		title = tk.Label(self, text="Select Spice Mix", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=3, sticky=tk.N)

        # scrollable frame for scrollable buttons
		frame = ScrollableFrame(self, width=1280, height=400, hscroll=False, vscroll=False, bg=bgColor)
		frame.grid(row=1, rowspan=2, column=0, columnspan=3, sticky=tk.S)


        # viewCustomWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel

		for spice in spices:
			button = tk.Button(
				frame,
				text = spice,
				font = smallFont,
				fg = fontColor,
				bg = buttonColor,
				activeforeground = pressedFont,
				activebackground = pressedButton,
				width = 340,
				height = 340,
				image = pixel,
				compound = tk.CENTER,
				command = lambda spice=spice: (
					controller.showFrame(viewCustomDetailsWin)
                )
            )
			button.grid(row=0, column=spices.index(spice), padx=10)
			

		frame.bind_children()
		frame.resize("fit_height")

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
            command = lambda: controller.showFrame(customMixesWin)
        )
		back.grid(row=3, column=1, columnspan=1)


# class for view details of custom mix window (view)
# WIP
class viewCustomDetailsWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x3 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

        # viewCustomDetailsWin title
		title = tk.Label(self, text="Spice 1", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=3, sticky=tk.N)
		
        # scrollable frame for scrollable labels
		frame = ScrollableFrame(self, width=1100, height=350, hscroll=False, vscroll=False, bg=buttonColor)
		frame.grid(row=1, rowspan=2, column=0, columnspan=3, sticky=tk.NS)
		frame.grid_columnconfigure(0, weight=1)
		frame.grid_columnconfigure(1, weight=1)


        # temporary array for testing
		spiceMix = [['Salt', 2, 'Tablespoons'], ['Black Pepper', 1, 'Tablespoons'], ['Spice 4', 1, 'Teaspoon'], ['Spice 8', 3, 'Tablespoons'], ['Spice 10', 1, 'Tablespoons']]
        
        # display spices in scrollable frame
		for spice in spiceMix:
			spiceName = tk.Label(
            frame,
            text=spice[0],
            font=regularFont,
            fg=fontColor,
            bg=buttonColor)
			spiceName.grid(row=spiceMix.index(spice), column=0, padx=10, pady=10, sticky=tk.W)
			
			spiceMeasurements = tk.Label(
                frame,
                text=str(spice[1]) + ' ' + spice[2],
                font=regularFont,
                fg=fontColor,
                bg=buttonColor)
			spiceMeasurements.grid(row=spiceMix.index(spice), column=1, padx=10, pady=10, sticky=tk.E)
			
		frame.bind_children()


        # viewCustomDetailsWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
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
            command = lambda: controller.showFrame(viewCustomWin)
        )
		back.grid(row=3, column=1, columnspan=1)


# class for view custom mixes window (remove)
# WIP
# NEED TO FIX BUTTON LABELS
class deleteCustomWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x3 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

        # deleteCustomWin title
		title = tk.Label(self, text="Select Spice Mix", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=3, sticky=tk.N)

        # scrollable frame for scrollable buttons
		frame = ScrollableFrame(self, width=1280, height=400, hscroll=False, vscroll=False, bg=bgColor)
		frame.grid(row=1, rowspan=2, column=0, columnspan=3, sticky=tk.S)


        # deleteCustomWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel

		for spice in spices:
			button = tk.Button(
				frame,
				text = spice,
				font = smallFont,
				fg = fontColor,
				bg = buttonColor,
				activeforeground = pressedFont,
				activebackground = pressedButton,
				width = 340,
				height = 340,
				image = pixel,
				compound = tk.CENTER,
				command = lambda spice=spice: (
					controller.showFrame(deleteWin)
                )
            )
			button.grid(row=0, column=spices.index(spice), padx=10)
			

		frame.bind_children()
		frame.resize("fit_height")

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
            command = lambda: controller.showFrame(customMixesWin)
        )
		back.grid(row=3, column=1, columnspan=1)


# class for remove custom mix window
# WIP
# NEED TO DISPLAY MIX NAME CORRECTLY
class deleteWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x5 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)

        # remove mix text
		removeTxt = tk.Label(self, text="Are you sure you\nwant to remove", font=titleFont, fg=fontColor, bg=bgColor)
		removeTxt.grid(row=1, column=1, columnspan=3, sticky=tk.S)

		mixTxt = tk.Label(self, text="Spice 1?", font=titleFont, fg=fontColor, bg=bgColor)
		mixTxt.grid(row=2, column=1, columnspan=3, sticky=tk.N)

        # remove GIF
		# TO BE ADDED
		
        # buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
		remove = tk.Button(
			self,
			text = "Remove",
			font = regularFont,
			fg = fontColor,
			bg = buttonColor,
			activeforeground = pressedFont,
			activebackground = pressedButton,
			width = 340,
			height = 100,
			image = pixel,
			compound = tk.CENTER,
			command = lambda: controller.showFrame(customMixesWin)

        )
		remove.grid(row=3, column=3, columnspan=1, sticky=tk.N)

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
            command = lambda: controller.showFrame(deleteCustomWin)
        )
		back.grid(row=3, column=1, columnspan=1, sticky=tk.N)
		

# class for view details of custom mix window (add)
# WIP
class addCustomDetailsWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x5 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)

        # addCustomDetailsWin title
		title = tk.Label(self, text="Adding Custom Mix", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=1, columnspan=3, sticky=tk.N)
		
        # scrollable frame for scrollable labels
		frame = ScrollableFrame(self, width=1100, height=350, hscroll=False, vscroll=False, bg=buttonColor)
		frame.grid(row=1, rowspan=2, column=1, columnspan=3, sticky=tk.NS)
		frame.grid_columnconfigure(0, weight=1)
		frame.grid_columnconfigure(1, weight=1)


        # temporary array for testing
		spiceMix = [['Salt', 2, 'Tablespoons'], ['Black Pepper', 1, 'Tablespoons'], ['Spice 4', 1, 'Teaspoon'], ['Spice 8', 3, 'Tablespoons'], ['Spice 10', 1, 'Tablespoons']]
        
        # display spices in scrollable frame
		for spice in spiceMix:
			spiceName = tk.Label(
            frame,
            text=spice[0],
            font=regularFont,
            fg=fontColor,
            bg=buttonColor)
			spiceName.grid(row=spiceMix.index(spice), column=0, padx=10, pady=10, sticky=tk.W)
			
			spiceMeasurements = tk.Label(
                frame,
                text=str(spice[1]) + ' ' + spice[2],
                font=regularFont,
                fg=fontColor,
                bg=buttonColor)
			spiceMeasurements.grid(row=spiceMix.index(spice), column=1, padx=10, pady=10, sticky=tk.E)
			
		frame.bind_children()


        # viewCustomDetailsWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
		cancel = tk.Button(
			self, 
            text = "Cancel", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customMixesWin)
        )
		cancel.grid(row=3, column=1, columnspan=1)
		
		add = tk.Button(
			self, 
            text = "Add Spice", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customSelectSpiceWin)
        )
		add.grid(row=3, column=2, columnspan=1)
		
		finish = tk.Button(
			self, 
            text = "Finish", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 340,
            height = 100,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customNameWin)
        )
		finish.grid(row=3, column=3, columnspan=1)
		

# class for spice selection window (add)
# WIP
class customSelectSpiceWin(tk.Frame):
	
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

        # customSelectSpiceWin title
		title = tk.Label(self, text="Select Spice", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=7, sticky=tk.N)

        # customSelectSpiceWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
        # button layout
		# |           |
		# | 0 1 2 3 4 |
		# | 5 6 7 8 9 |
		# |  confirm  |
		# note: text labels on buttons are determined by spices[1:10], not spices[0:9]

		button0 = tk.Button(
			self, 
            text = spices[1], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button0.grid(row=1, column=1, sticky=tk.N)
		
		button1 = tk.Button(
			self, 
            text = spices[2], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button1.grid(row=1, column=2, sticky=tk.N)
		
		button2 = tk.Button(
			self, 
            text = spices[3], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button2.grid(row=1, column=3, sticky=tk.N)
		
		button3 = tk.Button(
			self, 
            text = spices[4], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button3.grid(row=1, column=4, sticky=tk.N)
		
		button4 = tk.Button(
			self, 
            text = spices[5], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button4.grid(row=1, column=5, sticky=tk.N)

		button5 = tk.Button(
			self, 
            text = spices[6], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button5.grid(row=2, column=1, sticky=tk.N)
		
		button6 = tk.Button(
			self, 
            text = spices[7], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button6.grid(row=2, column=2, sticky=tk.N)
		
		button7 = tk.Button(
			self, 
            text = spices[8], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button7.grid(row=2, column=3, sticky=tk.N)
		
		button8 = tk.Button(
			self, 
            text = spices[9], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
        )
		button8.grid(row=2, column=4, sticky=tk.N)
		
		button9 = tk.Button(
			self, 
            text = spices[10], 
            font = smallFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: controller.showFrame(customAmountWin)
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
            command = lambda: controller.showFrame(addCustomDetailsWin)
        )
		back.grid(row=3, column=2, columnspan=3, sticky=tk.N)


# class for select amount window (add)
# WIP
class customAmountWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of select amount window
		self.configure(background=bgColor)
        # 4x5 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)

        # customAmountWin title
		title = tk.Label(self, text="Select Amount", font=titleFont, fg=fontColor, bg=bgColor)
		title.grid(row=0, column=0, columnspan=5, sticky=tk.N)

        # customAmountWin textbox
		self.amountBox = tk.Label(
			self,
			font = regularFont,
			fg = fontColor,
			bg = buttonColor,
			width = 10,
			text="0"
		)
		self.amountBox.grid(row=1, rowspan=1, column=2, columnspan=1, sticky=tk.N)

        # customAmountWin buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel

		plusOneButton = tk.Button(
			self, 
            text = "+1", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), 1)))
        )
		plusOneButton.grid(row=1, rowspan=1, column=3, columnspan=1, sticky=tk.NE, padx=10)
		
		plusFiveButton = tk.Button(
			self, 
            text = "+5", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), 5)))
        )
		plusFiveButton.grid(row=1, rowspan=1, column=4, columnspan=1, sticky=tk.NW)
		
		minusOneButton = tk.Button(
			self, 
            text = "-1", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), -1)))
        )
		minusOneButton.grid(row=1, rowspan=1, column=1, columnspan=1, sticky=tk.NW, padx=10)
		
		minusFiveButton = tk.Button(
			self, 
            text = "-5", 
            font = regularFont, 
            fg = fontColor, 
            bg = buttonColor, 
            activeforeground = pressedFont, 
            activebackground = pressedButton,
            width = 160,
            height = 160,
            image = pixel,
            compound = tk.CENTER,
            command = lambda: self.amountBox.config(text=str(backend.updateAmountGUI(int(self.amountBox.cget("text")), -5)))
        )
		minusFiveButton.grid(row=1, rowspan=1, column=0, columnspan=1, sticky=tk.NE)
		
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
            command = lambda: controller.showFrame(addCustomDetailsWin)
        )
		gramsButton.grid(row=2, column=0, columnspan=2, sticky=tk.N)
		
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
            command = lambda: controller.showFrame(addCustomDetailsWin)
        )
		teaspoonsButton.grid(row=2, column=2, sticky=tk.N)
		
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
            command = lambda: controller.showFrame(addCustomDetailsWin)
        )
		tablespoonsButton.grid(row=2, column=3, columnspan=2, sticky=tk.N)
		
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
            command = lambda: controller.showFrame(customSelectSpiceWin)
        )
		back.grid(row=3, column=2, sticky=tk.N)


# class for naming mix window (add)
# WIP
# NEED TO ADD LABEL TO DISPLAY NAME + ON-SCREEN KEYBOARD
class customNameWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x5 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)

        # text
		removeTxt = tk.Label(self, text="WIP\nEnter name of\ncustom spice:", font=titleFont, fg=fontColor, bg=bgColor)
		removeTxt.grid(row=1, column=1, columnspan=3, sticky=tk.S)
		
        # buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
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
			command = lambda: controller.showFrame(customMixesWin)

        )
		confirm.grid(row=3, column=3, columnspan=1, sticky=tk.N)

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
            command = lambda: controller.showFrame(customAmountWin)
        )
		back.grid(row=3, column=1, columnspan=1, sticky=tk.N)
		

# class for no spice error message window
class noSpiceWin(tk.Frame):
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
        # settings of window
		self.configure(background=bgColor)
        # 4x5 grid
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)
		self.columnconfigure(4, weight=1)

        # text
		removeTxt = tk.Label(self, text="ERROR:\nMissing Spice :(", font=titleFont, fg=fontColor, bg=bgColor)
		removeTxt.grid(row=1, column=1, columnspan=3, sticky=tk.S)

        # error GIF
		# TO BE ADDED
		
        # buttons
		self.pixel = tk.PhotoImage(width=1, height=1) # invisible pixel for button appearance
		pixel = self.pixel
		
		okay = tk.Button(
			self,
			text = "Okay",
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
		okay.grid(row=3, column=1, columnspan=3, sticky=tk.N)


# driver code
app = spiceItUpApp()
app.mainloop()
