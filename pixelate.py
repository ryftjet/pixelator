from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from math import floor, sqrt
from copy import deepcopy

WIDTH = 500
HEIGHT = 500

root = Tk()
root.geometry(f'{WIDTH}x{HEIGHT}')


class Pixelate:
    def __init__(self, root_):
        self.root = root_
        self.image = None
        self.pixelated_image = None
        self.image_to_show = None

        self.open_button = Button(root_, text='Open', command=lambda: self.add_image())
        self.open_button.place(x=WIDTH / 2 - 120, y=10)
        self.pixel_rate_entry = Entry(root_)
        self.pixel_rate_entry.place(x=WIDTH / 2 + 10, y=10)
        self.pixelate_button = Button(root_, text='Pixelate',
                                      command=lambda: self.decrease_pixel_quality(self.pixel_rate_entry.get()))
        self.pixelate_button.place(x=WIDTH / 2 - 60, y=10)
        self.size_label = Label(root_)
        self.image_label = Label(root_)
        self.image_label.place(x=0, y=100)

    def add_image(self):
        file_path = filedialog.askopenfilename()
        c_image = Image.open(file_path)
        size = int(c_image.size[0] / 5), int(c_image.size[1] / 5)
        c_image = c_image.resize(size)
        self.image = c_image
        c_image = ImageTk.PhotoImage(c_image)
        self.image_to_show = c_image
        self.image_label.configure(image=self.image_to_show)
        self.image_label.place(x=WIDTH / 2 - size[0] / 2, y=HEIGHT / 2 - size[1] / 2)
        self.size_label.place(x=WIDTH / 2, y=HEIGHT / 2 + size[1] / 2 + 20, anchor=CENTER)
        self.size_label.configure(text=f'{size[0]} x {size[1]}', justify=LEFT)

    def decrease_pixel_quality(self, depth=64):
        image_to_change = deepcopy(self.image)
        if depth == '' or depth == '0':
            depth = 64
        else:
            depth = int(depth)
        size = image_to_change.size
        x_off = divmod(size[0], int(sqrt(depth)))
        y_off = divmod(size[1], int(sqrt(depth)))
        for x in range(0, size[0] - x_off[1], int(sqrt(depth))):
            for y in range(0, size[1] - y_off[1], int(sqrt(depth))):
                list_of_pixels = []
                for a in range(int(sqrt(depth))):
                    for b in range(int(sqrt(depth))):
                        list_of_pixels.append((x + a, y + b))

                pixels = [image_to_change.getpixel((i, j)) for i, j in list_of_pixels]
                r = 0
                g = 0
                b = 0
                for pixel in pixels:
                    r += pixel[0]
                    g += pixel[1]
                    b += pixel[2]
                for i, j in list_of_pixels:
                    image_to_change.putpixel((i, j), (floor(r / depth), floor(g / depth), floor(b / depth)))
        self.pixelated_image = ImageTk.PhotoImage(image_to_change)
        self.image_label.configure(image=self.pixelated_image)
        self.size_label.configure(text=f'{size[0] / int(sqrt(depth))} x {size[1] / int(sqrt(depth))}')

    def loop(self):
        self.root.mainloop()


px = Pixelate(root)
px.loop()
