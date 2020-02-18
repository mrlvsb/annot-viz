import imageio
import numpy as np
import os
import pygame
import sys

from PIL import Image

COLOR_RED = (200, 0, 0)
COLOR_GREEN = (0, 200, 0)

COLOR_BACKGROUND = (30, 30, 30)


def print_help():
    print()
    print('anot-viz - A Tool to Vizualize Annotations')
    print()
    print('Usage:')
    print('pythom main.py <annotation-file> <directory with images corresponding to annotation-file>')
    print()


def load_image(filename, colorkey=None):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print('Cannot load image:', filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class AnnotationTimelineSprite(pygame.sprite.Sprite):

    def __init__(self, image : pygame.image):
        pygame.sprite.Sprite.__init__(self)
        self._image, self._rect = image, image.get_rect()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        self._rect = self._image.get_rect()

    @property
    def rect(self):
        return self._rect


class ImageSprite(pygame.sprite.Sprite):

    def __init__(self, image : pygame.image):
        pygame.sprite.Sprite.__init__(self)
        self._image, self._rect = image, image.get_rect()

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        self._image = image
        self._rect = self._image.get_rect()
        center_x, center_y = self._rect.center
        center_y += 50
        self._rect.center = (center_x, center_y)
        #self._rect.move_ip(0, 50)

    @property
    def rect(self):
        return self._rect


class Viz:

    def __init__(self):
        pygame.init()
        self.w = 500
        self.h = 500

        self.display = pygame.display.set_mode((self.w, self.h), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
        pygame.display.set_caption("Annot Viz")
        timeline_np_img, self.image, self.image_filenames = preprocess(*sys.argv[1:])
        self.current_image_index = 0

        self.timeline_np_img = timeline_np_img.transpose(1, 0, 2)
        self.timeline_image = pygame.surfarray.make_surface(self.timeline_np_img)

        self.annotation_timeline = AnnotationTimelineSprite(self.timeline_image)
        self.annotation_image = ImageSprite(self.image)

        self.timeline_sprite = pygame.sprite.RenderPlain((self.annotation_timeline))
        self.image_sprite = pygame.sprite.RenderPlain((self.annotation_image))


    #def on_root_resize(self, event):

    #def foo(self, annot_timeline_img : Image, image : Image):

    def display_next(self, amount=1):
        if len(self.image_filenames) > self.current_image_index + amount:
            self.current_image_index = self.current_image_index + amount
        else:
            self.current_image_index = 0

        self.image = pygame.image.load(os.path.join(sys.argv[2], self.image_filenames[self.current_image_index]))


    def display_prev(self, amount=1):
        if self.current_image_index - amount > 0:
            self.current_image_index = self.current_image_index - amount
        else:
            self.current_image_index = len(self.image_filenames) - amount

        self.image = pygame.image.load(os.path.join(sys.argv[2], self.image_filenames[self.current_image_index]))


    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            timeline_res = pygame.transform.scale(self.timeline_image, (self.w, 50))
            self.annotation_timeline.image = timeline_res

            image_res = pygame.transform.scale(self.image, (self.w, self.h - 50))
            self.annotation_image.image = image_res

            self.timeline_sprite.draw(self.display)
            self.image_sprite.draw(self.display)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button_l, button_m, button_r = pygame.mouse.get_pressed()
                    pos = pygame.mouse.get_pos()
                    #print('mouse:', pos)
                    #print(type(self.timeline_sprite))
                    #print(len(self.timeline_sprite))
                    #print(self.timeline_sprite.sprites())
                    clicked_sprites = [s for s in [*self.timeline_sprite.sprites(), *self.image_sprite.sprites()] if s.rect.collidepoint(pos)]
                    for s in clicked_sprites:
                        if isinstance(s, ImageSprite):
                            pos_x, pos_y = pos
                            if pos_x > self.w / 2:
                                if button_l:
                                    self.display_next()
                                elif button_r:
                                    self.display_next(24)
                            else:
                                if button_l:
                                    self.display_prev()
                                elif button_r:
                                    self.display_prev(24)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        pass
                    elif event.key == pygame.K_RIGHT:
                        self.display_next()
                    elif event.key == pygame.K_PAGEUP:
                        self.display_next(24)
                    elif event.key == pygame.K_LEFT:
                        self.display_prev()
                    elif event.key == pygame.K_PAGEDOWN:
                        self.display_prev(24)
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

    return annot_img, img, ls


def main():
    if len(sys.argv) == 3:
        #timeline_img, image = preprocess(*sys.argv[1:])
        viz = Viz()

        viz.run()
    else:
        print_help()


if __name__ == '__main__':
    main()