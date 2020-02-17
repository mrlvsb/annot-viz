import imageio
import numpy as np
import os
import pygame
import sys

from PIL import Image

COLOR_RED = (200, 0, 0)
COLOR_GREEN = (0, 200, 0)

COLOR_BACKGROUND = (30, 30, 30)


class Viz:

    def __init__(self):
        pygame.init()
        self.w = 500
        self.h = 500
        self.display = pygame.display.set_mode((self.w, self.h), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
        pygame.display.set_caption("Example resizable window")
        self.timeline_np_img, self.image = preprocess(*sys.argv[1:])

        self.t = self.timeline_np_img.transpose(1, 0, 2)
        self.surf = pygame.surfarray.make_surface(self.t)


    #def on_root_resize(self, event):

    #def foo(self, annot_timeline_img : Image, image : Image):

    def run(self):
        while True:
            #display.fill((255,255,255))

            surf_res = pygame.transform.scale(self.surf, (self.w, 50))

            self.display.blit(surf_res, (0, 0))

            self.display.blit(self.image, (0, 50))

            pygame.display.update()

            # Draw a red rectangle that resizes with the window.
            #pygame.draw.rect(display, (200,0,0), (display.get_width()/3,
            #display.get_height()/3, display.get_width()/3,
            #display.get_height()/3))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:
                        pass
                        #print(pygame.display.get_window_size())
                        #print('h: {}, w: {}'.format(pygame.display.get_height()), pygame.display.get_width())

                        #display = pygame.display.set_mode((event.w, event.h),
                        #                                  pygame.RESIZABLE)
                if event.type == pygame.VIDEORESIZE:
                    # There's some code to add back window content here.
                    # BUG: https://github.com/pygame/pygame/issues/201
                    self.w, self.h = event.w, event.h
                    old_display_saved = self.display
                    self.display = pygame.display.set_mode((self.w, self.h),
                                                           pygame.RESIZABLE)
                    self.display.blit(old_display_saved, (0, 0))
                    del old_display_saved


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
    
    return annot_img#Image.fromarray(annot_img)


def preprocess(annot_filename, imgs_dir):

    annot_img : np.ndarray
    img : Image

    #print(annot_filename, imgs_dir)

    if os.path.exists(imgs_dir):
        annotations = parse_anot_file(annot_filename)
        annot_img = create_annot_img(annotations, imgs_dir)

        imageio.imwrite('annot.png', Image.fromarray(annot_img))

        ls = os.listdir(imgs_dir)
        ls = sorted(ls)
        #img = Image.open(os.path.join(sys.argv[2], ls[0]))
        img = pygame.image.load(os.path.join(sys.argv[2], ls[0]))
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
    #
        viz.run()
    #
    #viz.root.mainloop()



    

if __name__ == '__main__':
    main()