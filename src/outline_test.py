import pygame
from pymunk.autogeometry import simplify_vertexes
from pymunk.vec2d import Vec2d
import triangulate

pygame.init()
window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

img = "damn.png"
print("Image:", img)
surface = pygame.image.load('.\\test_images\\' + img)
mask = pygame.mask.from_surface(surface)
v_outline = [Vec2d(float(p[0]), float(p[1])) for p in mask.outline(1)]


simplified_outline = simplify_vertexes(v_outline, 0.8)
del simplified_outline[-1]
outline_tuple = [(p[0], surface.get_height() - p[1]) for p in simplified_outline]
print("Original:", len(v_outline), "vertices")
print("Simplified:", len(simplified_outline), "vertices")
# print("Points:", len(points), "points")

window_center = window.get_rect().center
rect = surface.get_rect(center = window_center)
# window_points = [(p[0] + rect.x, p[1] + rect.y) for p in simplified_outline]


triangles = []
while len(simplified_outline) >= 3:
    ear = triangulate.GetEar(simplified_outline)
    if ear == []:
        break
    triangles.append(ear)
print("Triangles:", len(triangles), "triangles")

window_points = []
for triangle in triangles:
    for point in triangle:
        window_points.append((point[0] + rect.x, point[1] + rect.y))


# for triangle in triangles:
#     window_points.append((triangle.p0.x + rect.x, -triangle.p0.y + rect.y))
#     window_points.append((triangle.p1.x + rect.x, -triangle.p1.y + rect.y))
#     window_points.append((triangle.p2.x + rect.x, -triangle.p2.y + rect.y))

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    window.fill(0)
    # window.blit(surface, rect)
    # pygame.draw.lines(window, "white", True, window_points, 1)
    i = 0
    for tri in triangles:
        colors = [(50, 50, 50), (128, 128, 128), (105, 105, 105)]
        color = colors[i%3]
        pygame.draw.polygon(window, color, ((tri[0][0] + rect.x, tri[0][1] + rect.y),(tri[1][0] + rect.x, tri[1][1] + rect.y), (tri[2][0] + rect.x, tri[2][1] + rect.y)))
        i += 1
    pygame.display.flip()

pygame.quit()
exit()