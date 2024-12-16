# To-Do
# 1) Fix Collisions
# 2) Change to Delta Time

import pygame
import sys
import math

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

    def updateGravity(self):
        self.velocity.y += 0.35

    def getInput(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.velocity.y = -10

    def updatePosition(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
  
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class Tile:
    def __init__(self, x, y, color, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

def playerTileCollision():
    for tile in tileGroup:
        tempX = player.x
        tempY = player.y
        side = "none"
        if player.x < tile.x: # left edge
            tempX = tile.x
            side = "left"
        elif player.x > tile.x + tile.width: # right edge
            tempX = tile.x + tile.width
            side = "right"
        if player.y < tile.y: # top edge
            tempY = tile.y
            side = "top"
        elif player.y > tile.y + tile.height: # bottom edge
            tempY = tile.y + tile.height
            side = "bottom"

        distanceX = player.x - tempX
        distanceY = player.y - tempY
        distance = math.sqrt((distanceX*distanceX) + (distanceY*distanceY))
        if distance < player.radius:

            if side == "left" and player.velocity.x > 0:
                player.velocity.x = player.velocity.x * -1
            elif side == "right" and player.velocity.x < 0:
                player.velocity.x = player.velocity.x * -1
            if side == "top" and player.velocity.y > 0:
                player.velocity.y = -10
            elif side == "bottom" and player.velocity.y < 0:
                player.velocity.y = 0

# player
player = Player(48 * 5, 48, (255, 0, 0), 24)

# load map
map = open("map.txt", "r")
for rowIndex, rowIterable in enumerate(map.readlines()):
    for columnIndex, columnIterable in enumerate(rowIterable):
        if columnIterable == "1":
            tile = Tile(columnIndex * 48, rowIndex * 48, (0, 0, 0), 48, 48)
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
        player.updateGravity()

        player.getInput()

        playerTileCollision()

        player.updatePosition()

        # draw
        window.fill((255, 255, 255))

        player.draw(window)
        
        for tile in tileGroup:
            tile.draw(window)
        
        clock.tick(FPS)

        pygame.display.update()

if __name__ == "__main__":
  main()
