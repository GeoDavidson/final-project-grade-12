import random
import sys

import pygame

pygame.init()

WINDOW_WIDTH = 768 # 48 * 16
WINDOW_HEIGHT = 432 # 48 * 9

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gliding Game")

clock = pygame.time.Clock()
FPS = 60

tileGroup = []

class Player:
    def __init__(self, x, y, color, width, height):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

        self.velocity = pygame.Vector2(0, 0)

    def update(self):
        if pygame.key.get_pressed()[pygame.K_a]:
            if self.velocity.x > -4:
                self.velocity.x -= 0.5

        if pygame.key.get_pressed()[pygame.K_d]:
            if self.velocity.x < 4:
                self.velocity.x += 0.5
        
        self.x += self.velocity.x

        for tile in tileGroup:
            playerLeftEdge = player.x
            playerRightEdge = player.x + player.width
            playerTopEdge = player.y
            playerBottomEdge = player.y + player.height

            tileLeftEdge = tile.x
            tileRightEdge = tile.x + tile.width
            tileTopEdge = tile.y
            tileBottomEdge = tile.y + tile.height

            if playerLeftEdge < tileRightEdge and playerRightEdge > tileLeftEdge and playerTopEdge < tileBottomEdge and playerBottomEdge > tileTopEdge:
                if self.velocity.x < 0:
                    if pygame.key.get_pressed()[pygame.K_a]:
                        self.velocity.x = 0
                    else:
                        self.velocity.x *= -1 / 2
                    self.x = tile.x + tile.width
                elif self.velocity.x > 0:
                    if pygame.key.get_pressed()[pygame.K_d]:
                        self.velocity.x = 0
                    else:
                        self.velocity.x *= -1 / 2
                    self.x = tile.x - self.width

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.velocity.y -= 0.4
        else: 
            self.velocity.y += 0.4

        self.y += self.velocity.y

        for tile in tileGroup:
            playerLeftEdge = player.x
            playerRightEdge = player.x + player.width
            playerTopEdge = player.y
            playerBottomEdge = player.y + player.height

            tileLeftEdge = tile.x
            tileRightEdge = tile.x + tile.width
            tileTopEdge = tile.y
            tileBottomEdge = tile.y + tile.height

            if playerLeftEdge < tileRightEdge and playerRightEdge > tileLeftEdge and playerTopEdge < tileBottomEdge and playerBottomEdge > tileTopEdge:
                if self.velocity.y < 0:
                    self.velocity.y = 0
                    self.y = tile.y + tile.height
                elif self.velocity.y > 0:
                    self.velocity.y *= -1 / 2
                    self.y = tile.y - self.height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

class Tile:
    def __init__(self, x, y, color, width, height):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

player = Player(48 * 5, 48 * 4, (255, 0, 0), 32, 32)

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
