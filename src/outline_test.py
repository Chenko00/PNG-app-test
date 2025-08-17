import pygame
from pymunk.autogeometry import simplify_vertexes

pygame.init()
window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

img = "scug.png"
print("Image:", img)
surface = pygame.image.load('.\\test_images\\' + img)
mask = pygame.mask.from_surface(surface)
outline = mask.outline(1)
simplified_outline = simplify_vertexes(outline, 0.8)
del simplified_outline[-1]
print("Original:", len(outline), "vertices")
print("Simplified:", len(simplified_outline), "vertices")
window_center = window.get_rect().center
rect = surface.get_rect(center = window_center)
window_points = [(p[0] + rect.x, p[1] + rect.y) for p in simplified_outline]
# print(window_points)

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 

    
    

    window.fill(0)
    # window.blit(surface, rect)
    pygame.draw.lines(window, "white", True, window_points, 1)
    pygame.display.flip()

pygame.quit()
exit()