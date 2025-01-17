import os
import random
import sys

import pygame

pygame.init()

WINDOW_WIDTH = 36 * 21 # 756
WINDOW_HEIGHT = 36 * 15 # 540

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Gliding Game")

clock = pygame.time.Clock()
FPS = 60

menu = pygame.image.load(os.path.join("img", "menu.png")).convert_alpha()
menu.set_alpha(112)

font = pygame.font.Font(None, 36)

playerGroup = []
enemyGroup = []
tileGroup = []
launchTileGroup = []
killTileGroup = []
goldTileGroup = []

class Sprite:
    def __init__(self, x, y, color, width, height):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

class Player(Sprite):
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color, width, height)

        self.speed = 2
        self.maxSpeed = 3.8

        self.friction = 1.15
        self.wallFriction = 1.4

        self.wallJumpForceX = 12
        self.wallJumpForceY = -10

        self.wallJumpBufferTime = 0.1

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

        if -0.08 < self.velocity.x < 0.08:
            self.velocity.x = 0
        else:
            self.velocity.x = self.velocity.x / self.friction

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

        if self.x > window.get_width():
            self.x = -self.width
        elif self.x + self.width < 0:
            self.x = window.get_width()
        else:
            self.y += self.velocity.y
        
        if self.y > window.get_height():
            self.y = -self.height

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
                goldTileGroup.clear()
                level.current -= 1
                return None

        for enemy in enemyGroup:
            if collided(self, enemy):
                goldTileGroup.clear()
                level.current -= 1
                return None

        for goldTile in goldTileGroup:
            if collided(self, goldTile):
                goldTileGroup.remove(goldTile)
                return None


class Enemy(Sprite):
    def __init__(self, x, y, color, width, height):
        super().__init__(x, y, color, width, height)

        self.speed = 2.5
        self.direction = pygame.Vector2(random.choice([-1, 1]), 0)

    def update(self):
        if self.x > window.get_width():
            self.x = -self.width
        elif self.x + self.width < 0:
            self.x = window.get_width()
        elif self.y > window.get_height():
            self.direction.y = -1
        elif self.y + self.height < 0:
            self.direction.y = 1

        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed

        for tile in tileGroup:
            if collided(self, tile):
                if self.direction.x < 0: # left
                    self.direction.x = 0
                    self.direction.y = random.choice([-1, 1])
                    self.x = tile.x + tile.width
                elif self.direction.x > 0: # right
                    self.direction.x = 0
                    self.direction.y = random.choice([-1, 1])
                    self.x = tile.x - self.width

        for tile in tileGroup:
            if collided(self, tile):
                if self.direction.y < 0: # top
                    self.direction.x = random.choice([-1, 1])
                    self.direction.y = 0
                    self.y = tile.y + tile.height
                elif self.direction.y > 0: # bottom
                    self.direction.x = random.choice([-1, 1])
                    self.direction.y = 0
                    self.y = tile.y - self.height

class Level:
    def __init__(self):
        self.current = -1

    def clearLevel(self):
        playerGroup.clear()
        enemyGroup.clear()
        tileGroup.clear()
        launchTileGroup.clear()
        killTileGroup.clear()

    def loadLevel(self, levelName):
        map = open(levelName, "r")
        for rowIndex, rowIterable in enumerate(map.readlines()):
            for columnIndex, columnIterable in enumerate(rowIterable):
                if columnIterable == "T":
                    n = random.randint(0, 148)
                    tile = Sprite(columnIndex * 36, rowIndex * 36, (n, n, n), 36, 36)
                    tileGroup.append(tile)
                elif columnIterable == "L":
                    launchTile = Sprite(columnIndex * 36, rowIndex * 36 + 28, (0, 255, 0), 36, 8)
                    launchTileGroup.append(launchTile)
                elif columnIterable == "K":
                    killTile = Sprite(columnIndex * 36, rowIndex * 36 + 32, (255, 0, 0), 36, 4)
                    killTileGroup.append(killTile)
                elif columnIterable == "G":
                    goldTile = Sprite(columnIndex * 36 + 9, rowIndex * 36 + 9, (255,215,0), 18, 18)
                    goldTileGroup.append(goldTile)
                elif columnIterable == "E":
                    enemy = Enemy(columnIndex * 36, rowIndex * 36, (255, 0, 0), 36, 36)
                    enemyGroup.append(enemy)
                elif columnIterable == "P":
                    player = Player(columnIndex * 36 + 9, rowIndex * 36 + 9, (0, 0, 255), 18, 18)
                    playerGroup.append(player)
        map.close()

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

level = Level()

def main():
    background = (255, 255, 255)

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
        for player in playerGroup:
            player.update()

            if player.velocity.x == 0 and player.velocity.y == 0:
                value = background[1] - 5
                background = (background[0], max(0, value), max(0, value))
            else:
                value = background[1] + 3
                background = (background[0], min(255, value), min(255, value))

        for enemy in enemyGroup:
            enemy.update()

        if len(goldTileGroup) == 0:
            level.current += 1
            level.clearLevel()
            level.loadLevel(f"levels/level-{level.current}.txt")

        # draw
        window.fill(background)

        if level.current == 0:
            window.blit(menu, (0, 0))

        for player in playerGroup:
            player.draw(window)

        for tile in tileGroup:
            tile.draw(window)

        for enemy in enemyGroup:
            enemy.draw(window)

        for launchTile in launchTileGroup:
            launchTile.draw(window)

        for killTile in killTileGroup:
            killTile.draw(window)

        for goldTile in goldTileGroup:
            goldTile.draw(window)

        value = abs(background[1] - 255)
        levelText = font.render(f"{level.current}", True, (background[0], value, value))
        levelTextRect = levelText.get_rect(center=(18, 18))
        window.blit(levelText, levelTextRect)

        clock.tick(FPS)

        pygame.display.update()

if __name__ == "__main__":
  main()
