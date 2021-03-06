from tkinter import Tk, Button, Canvas, Label
from PIL import ImageTk, Image
from io import BytesIO
import random
import requests


class Window:
    def __init__(self, names=None, images=None, urls=None):
        self.name = None
        self.names = names
        self.images = images
        self.urls = urls
        self.prev = None

        self.root = Tk()
        self.root.title('Burton Guster')
        self.root.after(1, lambda: self.root.focus_force())
        self.root.resizable(False, False)

        self.wscreen = self.root.winfo_screenwidth()
        self.hscreen = self.root.winfo_screenheight()
        self.wscale = 1
        self.hscale = 1

        self.default_dims = (1920, 1080)
        if self.default_dims != (self.wscreen, self.hscreen):
            self.wscale = self.wscreen / self.default_dims[0]
            self.hscale = self.hscreen / self.default_dims[1]

        # Fixed size 500x500
        self.root.geometry(f'{int(500*self.wscale)}x{int(500*self.hscale)}')

        # Centers window
        x_offset = int(self.wscreen / 2 - 500*self.wscale / 2)
        y_offset = int(self.hscreen / 2 - 500*self.hscale / 2)
        self.root.geometry('+{}+{}'.format(x_offset, y_offset))

        # Create canvas
        self.canvas = Canvas(self.root, width=400*self.wscale, height=400*self.hscale)
        self.canvas.grid(row=0, padx=48*self.wscale, pady=10*self.hscale)
        self.image = self.canvas.create_image(200*self.wscale, 200*self.hscale, image=None)

        # Create label
        self.label = Label(self.root, text=None)
        self.label.configure(font=('Calibri', int(18*self.wscale)))
        self.label.grid(row=2, rowspan=2, sticky='NWSE')

        # Create button
        self.button = Button(self.root, text="Hear about Pluto?", command=self.update)
        self.button.configure(fg='#191970', activeforeground='white', bd=0, font=('Calibri', int(16*self.wscale)))
        self.button.configure(highlightthickness=0, highlightbackground='#708090')
        self.button.grid(row=4, pady=0.5*self.hscale, sticky='NWSE')

        # Default background
        default_bg = '#708090'
        self.root.configure(bg=default_bg)
        for widget in self.root.winfo_children():
            widget.configure(bg=default_bg)

        self.update()

    def update(self):
        """
        Updates current image and nickname
        :return: None
        """
        self.update_image()
        self.update_name()

    def update_image(self):
        """
        Modifies current image on canvas
        :return: None
        """
        try:
            url = self.get_url()
            while url == self.prev:
                url = self.get_url()
            self.prev = url
            response = requests.get(url)
            im = Image.open(BytesIO(response.content))

        except requests.ConnectionError as connection_err:
            print(f'Connection Error: {connection_err}')
            im = Image.open(self.get_image())

        fixed_scale = max(self.wscale, self.hscale)
        im = im.resize((int(403*fixed_scale), int(403*fixed_scale)), Image.ANTIALIAS)

        im = ImageTk.PhotoImage(im)
        self.canvas.itemconfig(self.image, image=im)
        self.canvas.image = im

    def update_name(self):
        """
        Modified current name on canvas
        :return: None
        """
        self.label.config(text=self.get_name())

    def get_image(self):
        return random.choice(self.images)

    def get_name(self):
        return random.choice(self.names)

    def get_url(self):
        return random.choice(self.urls)

    def run(self):
        self.root.mainloop()
