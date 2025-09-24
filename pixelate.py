from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showerror
from PIL import Image, ImageTk, UnidentifiedImageError
from math import floor, sqrt
from copy import deepcopy

WIDTH = 300
HEIGHT = 500


class PixelateApp:
    def __init__(self):
        # Set up window
        self.root = Tk()
        self.root.geometry(f'{WIDTH}x{HEIGHT}')
        self.root.title('Pixelator')

        # Set up image
        self.original_image = None
        self.pixelated_image = None
        self.image_to_show = None

        # Create button frame
        self.button_frame = Frame(self.root)
        self.button_frame.pack(side="top", fill="x")

        # Create the open button
        self.open_button = Button(
            self.button_frame,
            text='Open',
            command=lambda: self.add_image()
        )
        self.open_button.pack(side="left")

        # Create the pixel scale rate
        self.pixel_scale_rate = Scale(
            self.button_frame,
            orient="horizontal",
            from_=1,
            to=1000,
        )
        self.pixel_scale_rate.pack(fill="x")
        self.pixel_scale_rate.bind(
            "<ButtonRelease>",
            lambda _: self.decrease_pixel_quality()
        )

        self.image_label = Label(self.root)
        self.image_label.pack(side="bottom")
        self.size_label = Label(self.root)
        self.size_label.pack(side="bottom")

    def add_image(self) -> None:
        # Open the image file
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png')])
        try:
            self.original_image = Image.open(file_path)
        except FileNotFoundError:
            # No image selected, ignore
            return
        except UnidentifiedImageError:
            # Non-image selected
            showerror('Image Not Found', f'The selected file is not an image: {file_path}')
            return

        self.image_to_show = ImageTk.PhotoImage(self.original_image)
        # Disable inspections because self.image_to_show is technically not a Tkinter Image
        # noinspection PyTypeChecker
        self.image_label.configure(image=self.image_to_show)
        self.size_label.configure(text=f'{self.original_image.size[0]} x {self.original_image.size[1]}', justify="left")

        # Run the initial
        self.decrease_pixel_quality()

    def decrease_pixel_quality(self) -> None:
        """Pixelate the image"""
        # No image selected yet, do nothing
        if not self.original_image:
            return

        # Get the image and the depth
        image_to_change = deepcopy(self.original_image)
        depth = int(self.pixel_scale_rate.get())

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
        reduced_image = image_to_change.convert('P', palette=Image.Palette.ADAPTIVE, colors=50)
        self.pixelated_image = ImageTk.PhotoImage(reduced_image)
        # Disable inspections because self.image_to_show is technically not a Tkinter Image
        # noinspection PyTypeChecker
        self.image_label.configure(image=self.pixelated_image)
        self.size_label.configure(text=f'{size[0] // int(sqrt(depth))} x {size[1] // int(sqrt(depth))}')

    def loop(self) -> None:
        self.root.mainloop()


def main():
    app = PixelateApp()
    app.loop()


if __name__ == '__main__':
    main()
