import tkinter as tk


class NextPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="lightBlue")
        self.controller = controller

        self.label = tk.Label(self, text="Next Page", font=("Helvetica", 20), fg="black", bg="lightBlue")
        self.label.grid(row=10, column=10, padx=20, pady=20, sticky="w")

        self.button = tk.Button(
            self,
            text="Go Back",
            font=("Helvetica", 20),
            command=lambda: controller.show_frame("SpiceItUpPage")
        )
        self.button.grid(row=20, column=10, padx=20, pady=20, sticky="e")

        # make grid expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)


class SpiceItUpPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="lightBlue")
        self.controller = controller

        self.label = tk.Label(self, text="Spice It Up!", font=("Helvetica", 20), fg="black", bg="lightBlue")
        self.label.grid(row=10, column=10, padx=20, pady=20)

        self.button = tk.Button(
            self,
            text="Next Page",
            font=("Helvetica", 20),
            command=lambda: controller.show_frame("NextPage")
        )
        self.button.grid(row=20, column=10, padx=20, pady=20)

        # expand empty rows/cols
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)


class SpiceitUp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spice It Up!")
        self.geometry("1980x1080")
        self.configure(bg="lightBlue")

        # container frame
        container = tk.Frame(self, bg="lightBlue")
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F, name in [(SpiceItUpPage, "SpiceItUpPage"), (NextPage, "NextPage")]:
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=10, column=10, sticky="nsew")

        self.show_frame("SpiceItUpPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = SpiceitUp()
    app.mainloop()
