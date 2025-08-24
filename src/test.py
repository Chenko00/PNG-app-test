import sys, random
random.seed(1)
import pygame
import pymunk
import pymunk.pygame_util

from pymunk.autogeometry import simplify_vertexes as simplify_vertices
from triangulate import GetEar

import tkinter
import tkinter.filedialog

from typing import List
from typing import Tuple

def convert_to_triangles(outline):
    simplified_outline = simplify_vertices(outline, 0.8)
    del simplified_outline[-1]

    triangles = []
    while len(simplified_outline) >= 3:
        ear = GetEar(simplified_outline)
        if ear == []:
            break
        triangles.append(ear)
    
    return triangles

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

def is_png(file):
    return file.endswith('.png')

def add_ball(space):
    mass = 3
    radius = 25
    body = pymunk.Body()
    x = random.randint(120, 300)
    body.position = x, 50
    shape = pymunk.Circle(body, radius) 
    shape.mass = mass
    shape.friction = 1
    space.add(body, shape)
    return shape

class PNGShape():
    def __init__(self, file, screen):
        self.body = pymunk.Body()
        self.body.position = 50, 50
        img = pygame.image.load(file)
        img_mask = pygame.mask.from_surface(img)
        img_outline = img_mask.outline(1)
        triangles = convert_to_triangles(img_outline)
        window_center = screen.get_rect().center
        rect = img.get_rect(center = window_center)

        triangles_draw = []
        for triangle in triangles:
            triangle_tuple = tuple((p[0] + rect.x / 2, p[1] + rect.y / 2) for p in triangle)
            triangles_draw.append(triangle_tuple)
        
        self.shape: List [pymunk.Shape] = []
        for i in range (len(triangles)):
            # self.shape.append(pymunk.Segment(self.body, img_outline[i], img_outline[(i+1)%len(img_outline)], 3))
            self.shape.append(pymunk.Poly(self.body, triangles_draw[i]))
            self.shape[i].elasticity = 0.5
            self.shape[i].density = 1
            self.shape[i].friction = 1
    def add_shape(self, space):
        # print ("Added a shape with", len(self.shape), "triangles")
        space.add(self.body, *self.shape)
        return self.shape

def getImageOutline(file):
    img = pygame.image.load(file).convert_alpha()
    img_mask = pygame.mask.from_surface(img)
    return img_mask.outline()


def main():
    # pygame stuff
    pygame.init()
    running = True
    pygame.display.set_caption("PNG App Test")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    FPS = 60
    f = "<No File Selected>"

    # pymunk stuff
    space = pymunk.Space()
    space.gravity = (0.0, 980.0)

    # button stuff
    font = pygame.font.SysFont('Arial Black', 20)
    button_text = font.render('Select Image', True, 'black')
    button_height = 30
    button_width = 155
    button = pygame.Rect(10, 10, button_width, button_height)

    # balls
    balls = []
    ticks_to_next_ball = 10
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    # png shapes
    shapes = []
    # walls
    static: List[pymunk.Shape] = [
        pymunk.Segment(space.static_body, (0, 600), (0, 55), 5),
        pymunk.Segment(space.static_body, (0, 55), (800, 55), 5),
        pymunk.Segment(space.static_body, (800, 55), (800, 600), 5),
        pymunk.Segment(space.static_body, (0, 600), (800, 600), 5),
    ]

    for s in static:
        s.friction = 1.0
        s.group = 1
    space.add(*static)
    tick = 0
    image_added = False
    is_pointing_at_shape = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(event.pos):
                f = prompt_file()
                if is_png(f):
                    image_added = True
                    pngShape = PNGShape(f, screen)
                    pngShape.add_shape(space)
                    shapes.append(pngShape)
                else:
                    image_added = False
            if event.type == pygame.MOUSEBUTTONDOWN and is_pointing_at_shape:
                print("Clicked on a shape")
        mouse_pos = pymunk.pygame_util.get_mouse_pos(screen)
        max_distance = 5
        info = space.point_query_nearest(mouse_pos, max_distance, pymunk.ShapeFilter())
        if info is not None and isinstance(info.shape,pymunk.Poly):
            # print("Pointing over a shape at", mouse_pos)
            is_pointing_at_shape = True
        else:
            is_pointing_at_shape = False
        # if image_added and tick % FPS == 0:
        #     pngShape = PNGShape(f, screen)
        #     pngShape.add_shape(space)
        #     shapes.append(pngShape)
        space.step(1 / FPS)
        tick += 1
        # fill background with black color
        screen.fill((0, 0, 0))
        mouseY, mouseX = pygame.mouse.get_pos()
        if button.x <= mouseX <= button.x + button_height and button.y <= mouseY <= button.y + button_width:
            pygame.draw.rect(screen, ('red'), button)
        else:
            pygame.draw.rect(screen, ('white'), button)
        screen.blit(button_text, (button.x + 5, button.y))
        screen.blit(font.render("fps: " + str(clock.get_fps()), True, pygame.Color("white")), (200, 0))
        
        space.debug_draw(draw_options)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    sys.exit(main())