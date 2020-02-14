import imageio
import numpy as np
import os
import sys

from tkinter import *
from PIL import ImageTk, Image

COLOR_RED = (200, 0, 0)
COLOR_GREEN = (0, 200, 0)

COLOR_BACKGROUND = (30, 30, 30)


# Events: https://stackoverflow.com/questions/29211794/how-to-bind-a-click-event-to-a-canvas-in-tkinter
# Events: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm


def callback(event):
    print("clicked at", event.x, event.y)


class Viz:
    def __init__(self):
        self.root = Tk()
        self.canvas = Canvas(self.root, width = 300, height = 300)
        self.canvas.pack()

        self.root.bind('<Configure>', self.on_root_resize)
        #self.root.bind('<ButtonRelease-1>', self.on_root_resize)

        self.image_canvas = Canvas(self.root, width = 300, height = 300)
        self.image_canvas.pack()


    def on_root_resize(self, event):
        print("resize", event, event.width, event.height)
        
        annot_timeline_resized_img = self.timeline_img.resize((event.width - 2, 50), Image.ANTIALIAS)

        self.timg = ImageTk.PhotoImage(annot_timeline_resized_img)

        self.canvas.config(width=event.width - 2)

        self.canvas.create_image(0, 0, anchor=NW, image=self.timg)
        self.canvas.image = self.timg

        resized_image = self.image.resize((event.width - 2, event.height - 50 - 2), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(resized_image)

        self.image_canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.image_canvas.image = self.img




    def foo(self, annot_timeline_img : Image, image : Image):
        #self.img = ImageTk.PhotoImage(anot_timeline_img)
        #Image.open("/media/geordi/491194e1-de55-46bb-b049-a6121d476f62/abn/radosek_manual_crop_64_64/manual_crop_64_64_images/manual_crop_anomal_hd_30fps_01_faces/1.jpg"))

        #self.img = ImageTk.PhotoImage(Image.open("/media/geordi/491194e1-de55-46bb-b049-a6121d476f62/abn/radosek_manual_crop_64_64/manual_crop_64_64_images/manual_crop_anomal_hd_30fps_01_faces/1.jpg"))

        #print(self.canvas.winfo_width(), self.canvas.winfo_height())
        self.timeline_img = annot_timeline_img
        self.image = image
        
        annot_timeline_resized_img = self.timeline_img.resize((300, 50), Image.ANTIALIAS)
        self.timg = ImageTk.PhotoImage(annot_timeline_resized_img)

        self.canvas.create_image(0, 0, anchor=NW, image=self.timg)
        self.canvas.image = self.timg

        self.canvas.bind("<Button-1>", callback)


        image_resized_img = self.image.resize((300, 300 - 50 - 2), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image_resized_img)

        self.image_canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.image_canvas.image = self.img


def parse_anot_file(annot_filename):
    annotations : list = []

    with open(annot_filename, 'rt') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                start, end, *text = line.split()
                start, end = int(start), int(end)
                annotations.append((start, end))

    return annotations

def create_annot_img(annotations, imgs_dir):
    ls = os.listdir(imgs_dir)
    img_w : int = len(ls)
    annot_img = np.zeros([50, img_w, 3], np.uint8)
    annot_img[:, :] = COLOR_GREEN

    for start, end in annotations:
        #print(start, end)
        annot_img[:, start:end] = COLOR_RED
    
    return Image.fromarray(annot_img)


def preprocess(annot_filename, imgs_dir):

    annot_img : np.ndarray
    img : Image

    #print(annot_filename, imgs_dir)

    if os.path.exists(imgs_dir):
        annotations = parse_anot_file(annot_filename)
        annot_img = create_annot_img(annotations, imgs_dir)

        imageio.imwrite('annot.png', annot_img)

        ls = os.listdir(imgs_dir)
        ls = sorted(ls)
        img = Image.open(os.path.join(sys.argv[2], ls[0]))
    else:
        annot_img = np.zeros([50, 255, 3], np.uint8)

        #print(annot_img[0, 0])
        annot_img[0:10, :] = (255, 0, 0)

        imageio.imwrite('annot.png', annot_img)

    return annot_img, img


def main():
    if len(sys.argv) == 3:
        timeline_img, image = preprocess(*sys.argv[1:])
        viz = Viz()

        viz.foo(timeline_img, image)

    viz.root.mainloop()

if __name__ == '__main__':
    main()