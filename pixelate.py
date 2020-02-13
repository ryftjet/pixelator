from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from math import floor,sqrt
from copy import deepcopy

WIDTH = 500
HEIGHT = 500
root = Tk()
root.geometry(f'{WIDTH}x{HEIGHT}')

class Pixelate():
	def __init__(self, root):
		self.root = root
		self.image = None
		self.pxImage = None
		self.imageToShow = None

		self.openButton = Button(root, text='Open', command=lambda:self.AddImage())
		self.openButton.place(x=WIDTH/2-120, y=10)
		self.pixelRateEntry = Entry(root)
		self.pixelRateEntry.place(x=WIDTH/2+10, y=10)
		self.pixelateButton = Button(root, text='Pixelate', command=lambda:self.DecreasePixelQuality(self.pixelRateEntry.get()))
		self.pixelateButton.place(x=WIDTH/2-60, y=10)
		self.sizeLabel = Label(root)
		self.imageLabel = Label(root)
		self.imageLabel.place(x=0, y=100)

	def AddImage(self):
		filePath = filedialog.askopenfilename()
		cImage = Image.open(filePath)
		size = int(cImage.size[0]/5)  ,  int(cImage.size[1]/5)
		cImage = cImage.resize(size)
		self.image = cImage
		cImage = ImageTk.PhotoImage(cImage)
		self.imageToShow = cImage
		self.imageLabel.configure(image=self.imageToShow)
		self.imageLabel.place(x=WIDTH/2 - size[0]/2, y=HEIGHT/2 - size[1]/2)
		self.sizeLabel.place(x=WIDTH/2, y=HEIGHT/2 + size[1]/2+20, anchor=CENTER)
		self.sizeLabel.configure(text=f'{size[0]} x {size[1]}', justify=LEFT)

	def DecreasePixelQuality(self, depth = 64):
		imageToChange = deepcopy(self.image)
		if(depth == '' or depth == '0'): depth = 64
		else: depth = int(depth)
		size = imageToChange.size
		xOff = divmod(size[0], int(sqrt(depth)))
		yOff = divmod(size[1], int(sqrt(depth)))
		for x in range(0, size[0]-xOff[1], int(sqrt(depth))): #int(sqrt(depth))
			for y in range(0, size[1]-yOff[1], int(sqrt(depth))):
				listOfPixels = []
				for a in range(int(sqrt(depth))):
					for b in range(int(sqrt(depth))):
						listOfPixels.append((x+a, y+b))

				pixels = [imageToChange.getpixel((i,j)) for i,j in listOfPixels]
				r = 0
				g = 0
				b = 0
				for pixel in pixels:
					r += pixel[0]
					g += pixel[1]
					b += pixel[2]
				for i, j in listOfPixels:
					imageToChange.putpixel((i,j), (floor(r/depth),floor(g/depth),floor(b/depth)))
		self.pxImage = ImageTk.PhotoImage(imageToChange)
		self.imageLabel.configure(image=self.pxImage)
		self.sizeLabel.configure(text=f'{size[0]/int(sqrt(depth))} x {size[1]/int(sqrt(depth))}')

	def Loop(self):
		self.root.mainloop()
		
px = Pixelate(root)
px.Loop()