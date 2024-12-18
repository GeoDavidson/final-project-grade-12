import pygame
import sys
import math
import random

pygame.init()

WINDOW_WIDTH = 768 # 48 * 16
WINDOW_HEIGHT = 432 # 48 * 9

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gliding Game")

clock = pygame.time.Clock()
FPS = 60

tileGroup = []

class Player:
    def __init__(self, x, y, color, radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius

        self.velocity = pygame.Vector2(3, 0)
        self.nearestTile = pygame.Vector2(0, 0)

    def update(self):
        self.velocity.y += 0.6

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.velocity.y = -10

        tileDistance = 1000
        tileIndex = 0
        for i in range(len(tileGroup)):
            d = math.sqrt(((tileGroup[i].x + 24) - self.x) ** 2 + ((tileGroup[i].y + 24) - self.y) ** 2)
            if d < tileDistance:
                tileDistance = d
                tileIndex = i
        
        self.nearestTile.x = tileGroup[tileIndex].x + 24
        self.nearestTile.y = tileGroup[tileIndex].y + 24

        nearestX = max(tileGroup[tileIndex].x, min(self.x, tileGroup[tileIndex].x + tileGroup[tileIndex].width))
        nearestY = max(tileGroup[tileIndex].y, min(self.y, tileGroup[tileIndex].y + tileGroup[tileIndex].height))

        distance = math.sqrt((nearestX - self.x) ** 2 + (nearestY - self.y) ** 2)
        if distance <= self.radius:
            left = abs((self.x + self.radius) - tileGroup[tileIndex].x)
            right = abs((self.x - self.radius) - (tileGroup[tileIndex].x + tileGroup[tileIndex].width))
            top = abs((self.y + self.radius) - tileGroup[tileIndex].y)
            bottom = abs((self.y - self.radius) - (tileGroup[tileIndex].y + tileGroup[tileIndex].height))

            if left < right and left < top and left < bottom and self.velocity.x > 0:
                print("LEFT")
                self.velocity.x = self.velocity.x * -1
                self.x = tileGroup[tileIndex].x - self.radius
            elif right < left and right < top and right < bottom and self.velocity.x < 0:
                print("RIGHT")
                self.velocity.x = self.velocity.x * -1
                self.x = tileGroup[tileIndex].x + tileGroup[tileIndex].width + self.radius
            elif top < left and top < right and top < bottom and self.velocity.y > 0:
                print("TOP")
                self.velocity.y = self.velocity.y / -1.35
                self.y = tileGroup[tileIndex].y - self.radius
            elif bottom < left and bottom < right and bottom < top and self.velocity.y < 0:
                print("BOTTOM")
                self.velocity.y = 0
                self.y = tileGroup[tileIndex].y + tileGroup[tileIndex].width + self.radius
        
        self.x += self.velocity.x
        self.y += self.velocity.y


    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        pygame.draw.line(window, (0, 0, 255), (self.x, self.y), self.nearestTile)

class Tile:
    def __init__(self, x, y, color, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

# player
player = Player(48 * 5, 48, (255, 0, 0), 24)

# load map
map = open("map.txt", "r")
for rowIndex, rowIterable in enumerate(map.readlines()):
    for columnIndex, columnIterable in enumerate(rowIterable):
        if columnIterable == "1":
            n = random.randint(0, 148)
            tile = Tile(columnIndex * 48, rowIndex * 48, (n, n, n), 48, 48)
            tileGroup.append(tile)
map.close()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # update
        player.update()

        # draw
        window.fill((255, 255, 255))

        player.draw(window)
        
        for tile in tileGroup:
            tile.draw(window)
        
        clock.tick(FPS)

        pygame.display.update()

if __name__ == "__main__":
  main()
