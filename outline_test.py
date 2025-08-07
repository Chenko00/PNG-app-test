import pygame

pygame.init()
window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

surface = pygame.image.load('D:\VR Download\PNG app test\\star.png')
mask = pygame.mask.from_surface(surface)
outline = mask.outline(1)
window_center = window.get_rect().center
rect = surface.get_rect(center = window_center)
window_points = [(p[0] + rect.x, p[1] + rect.y) for p in outline]
print(window_points)

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