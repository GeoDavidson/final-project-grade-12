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

        self.velocity = pygame.Vector2(6, 0)

        self.nearestTile = pygame.Vector2(0, 0)
        self.nearestPosition = pygame.Vector2(0, 0)

    def update(self):
        tile = min(tileGroup, key=lambda tile: math.sqrt(((tile.x + tile.width / 2) - self.x) ** 2 + ((tile.y + tile.height / 2) - self.y) ** 2))

        nearestX = max(tile.x, min(self.x, tile.x + tile.width))
        nearestY = max(tile.y, min(self.y, tile.y + tile.height))

        self.nearestTile.x = tile.x + tile.width / 2
        self.nearestTile.y = tile.y + tile.height / 2
        self.nearestPosition.x = nearestX
        self.nearestPosition.y = nearestY

        distance = math.sqrt((nearestX - self.x) ** 2 + (nearestY - self.y) ** 2)
        if distance <= self.radius:
            left = abs((self.x + self.radius) - tile.x)
            right = abs((self.x - self.radius) - (tile.x + tile.width))
            top = abs((self.y + self.radius) - tile.y)
            bottom = abs((self.y - self.radius) - (tile.y + tile.height))

            if left < right and left < top and left < bottom and self.velocity.x >= 0: # left
                # self.velocity.x = self.velocity.x * -1 / 2
                self.velocity.x = self.velocity.x * -1
                if self.velocity.x > -1:
                    self.velocity.x = 0
                self.x += distance - self.radius
            elif right < left and right < top and right < bottom and self.velocity.x <= 0: # right
                # self.velocity.x = self.velocity.x * -1 / 2
                self.velocity.x = self.velocity.x * -1
                if self.velocity.x < 1:
                    self.velocity.x = 0
                self.x -= distance - self.radius
            elif top < left and top < right and top < bottom and self.velocity.y >= 0: # top
                # self.velocity.y = self.velocity.y / -2
                self.velocity.y = -11
                if self.velocity.y > -1:
                    self.velocity.y = 0
                self.y += distance - self.radius
            elif bottom < left and bottom < right and bottom and self.velocity.y < 0: # bottom
                self.velocity.y = self.velocity.y / -2
                if self.velocity.y < 1:
                    self.velocity.y = 0
                self.y -= distance - self.radius

        if pygame.key.get_pressed()[pygame.K_a]:
            if self.velocity.x > -4.5:
                self.velocity.x -= 0.4

        if pygame.key.get_pressed()[pygame.K_d]:
            if self.velocity.x < 4.5:
                self.velocity.x += 0.4

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.velocity.y -= 0.35
        else:
            self.velocity.y += 0.35

        self.y += self.velocity.y
        self.x += self.velocity.x


    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        pygame.draw.line(window, (0, 255, 0), (self.x, self.y), self.nearestTile)
        pygame.draw.line(window, (0, 0, 255), (self.x, self.y), self.nearestPosition)

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
player = Player(48 * 5, 48 * 5, (255, 0, 0), 24)

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
