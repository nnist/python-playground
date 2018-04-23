from tkinter import *
from tkinter.ttk import *
import threading
import time
import math

class App():
    def __init__(self, master):
        master.title('much visual')

        # Canvas
        w = Canvas(master, width=200, height=200)
        w.grid(row=0, column=0, rowspan=5, columnspan=2)
        w.create_rectangle(1, 1, 200, 200, fill='')
        
        self.cubes = []
        for i in range(100):
            rect = w.create_rectangle(1, 1, 2, 2, fill='red')
            cube = Cube(w, rect)
            cube.x = i * 2
            cube.offset = i * 0.2
            self.cubes.append(cube)

        # Offset field
        self.offset_label = Label(master, text='offset')
        self.offset_label.grid(column=0, row=6)
        self.offset_field = Entry(master)
        self.offset_field.insert(0, '0.2')
        self.offset_field.grid(column=1, row=6)

        # Amplitude field
        self.amp_label = Label(master, text='amplitude')
        self.amp_label.grid(column=0, row=7)
        self.amp_field = Entry(master)
        self.amp_field.insert(0, '10.0')
        self.amp_field.grid(column=1, row=7)

        # Normal buttons
        button = Button(master, text='Exit',command=master.destroy)
        button.grid(column=0, columnspan=2)

        self.t = threading.Timer(.05, self.update)
        self.t.start()

    def update(self):
        for i in range(len(self.cubes)):
            cube = self.cubes[i]
            try:
                offset = float(self.offset_field.get())
            except:
                offset = 0.2
            try:
                amp = float(self.amp_field.get())
            except:
                amp = 10.0
            cube.offset = i * offset
            cube.amplitude = amp
            cube.draw()

        self.t = threading.Timer(.1, self.update)
        self.t.start()

class Cube():
    def __init__(self, canvas, rect):
        self.x = 100
        self.y = 100
        self.offset = 0
        self.amplitude = 0
        self.canvas = canvas
        self.rect = rect

    def draw(self):
        self.y = 100 + math.sin(time.time() + self.offset) * self.amplitude
        self.canvas.coords(self.rect, (self.x, self.y, self.x+1, self.y+1))

top = Tk()
top.style = Style()
top.style.theme_use('clam')

app = App(top)
top.mainloop()
