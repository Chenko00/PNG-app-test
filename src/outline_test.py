import pygame
from pymunk.autogeometry import simplify_vertexes as simplify_vertices
from pymunk.vec2d import Vec2d
import triangulate

pygame.init()
window = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

img = "spike.png"
print("Image:", img)
surface = pygame.image.load('.\\test_images\\' + img)
mask = pygame.mask.from_surface(surface)
v_outline = [Vec2d(float(p[0]), float(p[1])) for p in mask.outline(1)]
if (len(v_outline) > 1000):
    tolerance = 0.9
else:
    tolerance = 0.8
simplified_outline = simplify_vertices(v_outline, tolerance)
del simplified_outline[-1]

print("Original:", len(v_outline), "vertices")
print("Simplified:", len(simplified_outline), "vertices")

window_center = window.get_rect().center
rect = surface.get_rect(center = window_center)

triangles = []
while len(simplified_outline) >= 3:
    ear = triangulate.GetEar(simplified_outline)
    if ear == []:
        break
    triangles.append(ear)
print("Triangles:", len(triangles), "triangles")

triangle_draw = []
for triangle in triangles:
    triangle_tuple = tuple((p[0] + rect.x, p[1] + rect.y) for p in triangle)
    triangle_draw.append(triangle_tuple)


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
    for tri in triangle_draw:
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        color = colors[i%3]
        # pygame.draw.polygon(window, color, ((tri[0]),(tri[1]), (tri[2])))
        pygame.draw.polygon(window, color, tri)
        i += 1
    pygame.display.flip()

pygame.quit()
exit()