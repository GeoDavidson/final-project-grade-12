import random
import sys

import pygame

pygame.init()

WINDOW_WIDTH = 36 * 21
WINDOW_HEIGHT = 36 * 15

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

        self.grounded = False
        self.launched = False
        self.spaceHeld = False

        self.direction = 0

        self.wallJumpStrafeTimer = 0
        self.wallJumpBufferTimer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.wallJumpStrafeTimer <= 0:
            if self.velocity.x > -4:
                self.velocity.x -= 2

        if keys[pygame.K_d] and self.wallJumpStrafeTimer <= 0:
            if self.velocity.x < 4:
                self.velocity.x += 2

        if self.wallJumpStrafeTimer <= 0:
            self.velocity.x /= 1.15

        self.wallJumpStrafeTimer -= 1 / 60

        if keys[pygame.K_SPACE] and not self.spaceHeld and not self.grounded and self.wallJumpBufferTimer > 0:
            self.spaceHeld = True
            self.wallJumpBufferTimer = 0
            self.velocity.x = self.direction * 6
            self.velocity.y = -10
            self.wallJumpStrafeTimer = 0.2
        
        self.wallJumpBufferTimer -= 1 / 60

        self.x += self.velocity.x

        for tile in tileGroup:
            if collided(self, tile):
                self.wallJumpStrafeTimer = 0
                if self.velocity.x < 0:
                    self.velocity.x = 0
                    self.direction = 1
                    if keys[pygame.K_a]:
                        self.wallJumpBufferTimer = 0.12
                        if self.velocity.y > 1.6:
                            self.velocity.y = 1.6
                    self.x = tile.x + tile.width
                elif self.velocity.x > 0:
                    self.velocity.x = 0
                    self.direction = -1
                    if keys[pygame.K_d]:
                        self.wallJumpBufferTimer = 0.12
                        if self.velocity.y > 1.6:
                            self.velocity.y = 1.6

                    self.x = tile.x - self.width

        if not keys[pygame.K_SPACE]:
            self.spaceHeld = False

        if self.velocity.y > 0:
            self.velocity.y += 0.8
            self.grounded = False
        elif keys[pygame.K_SPACE]:
            if self.grounded and not self.spaceHeld:
                self.grounded = False
                self.spaceHeld = True
                self.velocity.y = -10
            self.velocity.y += 0.55
        else:
            if self.launched:
                self.velocity.y += 0.55
            else:
                self.velocity.y += 1.6

        if self.velocity.y >= 8:
            self.velocity.y = 8

        self.y += self.velocity.y

        for tile in tileGroup:
            if collided(self, tile):
                self.wallJumpStrafeTimer = 0
                if self.velocity.y < 0:
                    self.velocity.y = 0
                    self.y = tile.y + tile.height
                elif self.velocity.y > 0:
                    self.grounded = True
                    self.launched = False

                    self.wallJumpBufferTimer = 0

                    self.velocity.y = 0
                    self.y = tile.y - self.height

        for launchTile in launchTileGroup:
            if collided(self, launchTile):
                self.grounded = False
                self.launched = True

                self.velocity.y = -12
                return None

        for killTile in killTileGroup:
            if collided(self, killTile):
                loadLevel("map.txt")
                return None

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
                tile = Tile(columnIndex * 36, rowIndex * 36, (n, n, n), 36, 36)
                tileGroup.append(tile)
            elif columnIterable == "L":
                launchTile = Tile(columnIndex * 36, rowIndex * 36 + 28, (0, 255, 0), 36, 8)
                launchTileGroup.append(launchTile)
            elif columnIterable == "K":
                killTile = Tile(columnIndex * 36, rowIndex * 36 + 32, (255, 0, 0), 36, 4)
                killTileGroup.append(killTile)
            elif columnIterable == "P":
                player = Player(columnIndex * 36, rowIndex * 36, (255, 0, 0), 12, 18)
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
