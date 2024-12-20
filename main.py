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

        self.speed = 2
        self.maxSpeed = 3.8

        self.friction = 1.15
        self.wallFriction = 1.4

        self.wallJumpForceX = 12
        self.wallJumpForceY = -10

        self.wallJumpBufferTime = 0.12

        self.jumpForce = -10

        self.defaultGravity = 0.775
        self.jumpGravity = 0.55
        self.upwardsGravity = 1.6

        self.maxFallSpeed = 8

        self.launchPadJumpForce = -14

        self.wallJumpForceXValue = self.wallJumpForceX

        self.velocity = pygame.Vector2(0, 0)

        self.grounded = False
        self.launched = False
        self.spaceHeld = False

        self.wallJumpDirection = 0
        self.wallJumpBufferTimer = 0
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.velocity.x > -self.maxSpeed:
                self.velocity.x -= self.speed

        if keys[pygame.K_d]:
            if self.velocity.x < self.maxSpeed:
                self.velocity.x += self.speed

        self.velocity.x /= self.friction

        if keys[pygame.K_SPACE] and not self.spaceHeld and not self.grounded and self.wallJumpBufferTimer > 0:
            self.spaceHeld = True
            self.wallJumpBufferTimer = 0
            self.velocity.x = self.wallJumpForceX
            self.velocity.y = self.wallJumpForceY

        self.wallJumpBufferTimer -= 1 / 60

        self.x += self.velocity.x

        for tile in tileGroup:
            if collided(self, tile):
                if self.velocity.x < 0: # left
                    self.velocity.x = 0
                    self.x = tile.x + tile.width

                    if keys[pygame.K_a]:
                        self.wallJumpForceX = self.wallJumpForceXValue
                        self.wallJumpBufferTimer = self.wallJumpBufferTime
                        if self.velocity.y > self.wallFriction:
                            self.velocity.y = self.wallFriction
                elif self.velocity.x > 0: # right
                    self.velocity.x = 0
                    self.x = tile.x - self.width

                    if keys[pygame.K_d]:
                        self.wallJumpForceX = -self.wallJumpForceXValue
                        self.wallJumpBufferTimer = self.wallJumpBufferTime
                        if self.velocity.y > self.wallFriction:
                            self.velocity.y = self.wallFriction

        if not keys[pygame.K_SPACE]:
            self.spaceHeld = False

        if self.velocity.y > 0:
            self.velocity.y += self.defaultGravity
            self.grounded = False
        elif keys[pygame.K_SPACE]:
            if self.grounded and not self.spaceHeld:
                self.grounded = False
                self.spaceHeld = True
                self.velocity.y = self.jumpForce
            self.velocity.y += self.jumpGravity
        else:
            if self.launched:
                self.velocity.y += self.jumpGravity
            else:
                self.velocity.y += self.upwardsGravity

        if self.velocity.y >= self.maxFallSpeed:
            self.velocity.y = self.maxFallSpeed

        self.y += self.velocity.y

        for tile in tileGroup:
            if collided(self, tile):
                if self.velocity.y < 0: # top
                    self.velocity.y = 0
                    self.y = tile.y + tile.height
                elif self.velocity.y > 0: # bottom
                    self.velocity.y = 0
                    self.y = tile.y - self.height

                    self.grounded = True
                    self.launched = False
                    self.wallJumpBufferTimer = 0

        for launchTile in launchTileGroup:
            if collided(self, launchTile):
                self.grounded = False
                self.launched = True
                self.velocity.y = self.launchPadJumpForce
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
