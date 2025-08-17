import sys, random
random.seed(1)
import pygame
import pymunk
import pymunk.pygame_util
import tkinter
import tkinter.filedialog

from typing import List
from typing import Tuple

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

def isPNG(file):
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
    def __init__(self, file):
        self.body = pymunk.Body()
        self.body.position = 50, 50
        img = pygame.image.load(file).convert_alpha()
        img_mask = pygame.mask.from_surface(img)
        img_outline = img_mask.outline(5)
        self.shape: List [pymunk.Shape] = []
        for i in range (len(img_outline)):
            self.shape.append(pymunk.Segment(self.body, img_outline[i], img_outline[(i+1)%len(img_outline)], 3))
            self.shape[i].elasticity = 0.4
            self.shape[i].density = 1
            self.shape[i].friction = 1
    def add_shape(self, space):
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
                if isPNG(f):
                    pngShape = PNGShape(f)
                    pngShape.add_shape(space)
                    shapes.append(pngShape)
                    # body = pymunk.Body(mass=1, moment=1000)
                    # body.position = (100, 200)
                    # body.apply_impulse_at_local_point((100, 0), (0, 1))
                    # listshape: List [pymunk.Shape] = []
                    # shapestest: List [Tuple[int, int]] = [
                    #     (0, 0), (40, 0), (40, 40), (0, 40), (20, 20)
                    # ]
                    # for i in range(len(shapestest)): 
                    #     listshape.append(pymunk.Segment(body,shapestest[i], shapestest[(i+1)%len(shapestest)], radius=5))
                    #     listshape[i].elasticity = 1
                    #     listshape[i].friction = 1

                    # space.add(body, *listshape)
                    
                    
                    
                    # shape = pymunk.Segment(body, (-50, 0), (50, 0), radius=10)
                    # shape.elasticity = 0.999
                    # space.add(body, shape)
                    # print(listshape[0].body)
                    # s1 = pymunk.Segment(space.static_body,(60, 60), (80, 80), 5)

                    
                    # img = pygame.image.load(f).convert_alpha()
                    # img_mask = pygame.mask.from_surface(img)
                    # img_outline = img_mask.outline()
                    # screen_center = screen.get_rect().center
                    # img_rect = img.get_rect(center = screen_center)
                    # screen_points = [(p[0] + img_rect.x, p[1] + img_rect.y) for p in img_outline]
        space.step(1 / FPS)
        # fill background with black color
        screen.fill((0, 0, 0))
        # if isPNG(f):
        #     pygame.draw.lines(screen, 'white', True, screen_points, 5)
        

        # ticks_to_next_ball -= 1
        # if ticks_to_next_ball <= 0:
        #     ticks_to_next_ball = 25
        #     ball_shape = add_ball(space)
        #     balls.append(ball_shape)
        
        

        mouseY, mouseX = pygame.mouse.get_pos()
        if button.x <= mouseX <= button.x + button_height and button.y <= mouseY <= button.y + button_width:
            pygame.draw.rect(screen, ('red'), button)
        else:
            pygame.draw.rect(screen, ('white'), button)
        screen.blit(button_text, (button.x + 5, button.y))
        
        space.debug_draw(draw_options)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    sys.exit(main())