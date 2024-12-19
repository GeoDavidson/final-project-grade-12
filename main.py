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

playerGroup = []
tileGroup = []
launchTileGroup = []
killTileGroup = []

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
                self.velocity.x -= 1

        if pygame.key.get_pressed()[pygame.K_d]:
            if self.velocity.x < 4:
                self.velocity.x += 1

        self.velocity.x /= 1.1
        self.x += self.velocity.x

        for tile in tileGroup:
            if collided(self, tile):
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

        if pygame.key.get_pressed()[pygame.K_w]:
            self.velocity.y -= 0.425
        else: 
            self.velocity.y += 0.425

        self.y += self.velocity.y

        for tile in tileGroup:
            if collided(self, tile):
                if self.velocity.y < 0:
                    self.velocity.y = 0
                    self.y = tile.y + tile.height
                elif self.velocity.y > 0:
                    self.velocity.y *= -1 / 2
                    self.y = tile.y - self.height

        for launchTile in launchTileGroup:
            if collided(self, launchTile):
                self.velocity.y = -12

        for killTile in killTileGroup:
            if collided(self, killTile):
                loadLevel("map.txt")

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

def collided(thing1, thing2):
    LeftEdge1 = thing1.x
    RightEdge1 = thing1.x + thing1.width
    TopEdge1 = thing1.y
    BottomEdge1 = thing1.y + thing1.height

    LeftEdge2 = thing2.x
    RightEdge2 = thing2.x + thing2.width
    TopEdge2 = thing2.y
    BottomEdge2 = thing2.y + thing2.height

    if LeftEdge1 < RightEdge2 and RightEdge1 > LeftEdge2 and TopEdge1 < BottomEdge2 and BottomEdge1 > TopEdge2:
        return True
    return False

def loadLevel(levelName):
    playerGroup.clear()
    tileGroup.clear()
    launchTileGroup.clear()
    killTileGroup.clear()

    map = open(levelName, "r")
    for rowIndex, rowIterable in enumerate(map.readlines()):
        for columnIndex, columnIterable in enumerate(rowIterable):
            if columnIterable == "T":
                n = random.randint(0, 148)
                tile = Tile(columnIndex * 48, rowIndex * 48, (n, n, n), 48, 48)
                tileGroup.append(tile)
            elif columnIterable == "L":
                launchTile = Tile(columnIndex * 48, rowIndex * 48 + 40, (0, 255, 0), 48, 8)
                launchTileGroup.append(launchTile)
            elif columnIterable == "K":
                killTile = Tile(columnIndex * 48, rowIndex * 48 + 44, (255, 0, 0), 48, 4)
                killTileGroup.append(killTile)
            elif columnIterable == "P":
                player = Player(columnIndex * 48, rowIndex * 48, (255, 0, 0), 24, 24)
                playerGroup.append(player)
    map.close()

def main():

    loadLevel("map.txt")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    loadLevel("map.txt")

        # update
        for player in playerGroup:
            player.update()

        # draw
        window.fill((255, 255, 255))

        for player in playerGroup:
            player.draw(window)
        
        for tile in tileGroup:
            tile.draw(window)
        
        for launchTile in launchTileGroup:
            launchTile.draw(window)

        for killTile in killTileGroup:
            killTile.draw(window)
        
        clock.tick(FPS)

        pygame.display.update()

if __name__ == "__main__":
  main()
