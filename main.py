import os
import time
import keyboard
import random
import math


class Board:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.cache: list[list[str]]

    def clear(self):
        self.cache = []

        char = "#"

        self.cache.append([char] * (self.y + 2))

        for _ in range(self.x):
            self.cache.append([char] + self.y * [" "] + [char])

        self.cache.append([char] * (self.y + 2))

    def set_char(self, x, y, char):
        self.cache[x + 1][y + 1] = char

    def __repr__(self) -> str:
        napis = ""
        for row in range(self.y + 2):
            row_napis = ""

            for column in range(self.x + 2):
                row_napis += self.cache[column][row]

            napis += row_napis + "\n"

        return napis


class Paddle:
    def __init__(self, map: Board) -> None:
        self.speedX = 1
        self.posX = int(math.ceil(map.x / 2)) - 1
        self.char = "-"
        map.set_char(self.posX, map.y - 1, self.char)
        map.set_char(self.posX + 1, map.y - 1, self.char)
        map.set_char(self.posX - 1, map.y - 1, self.char)
        self.map = map

    def changePosLeft(self):
        if self.posX - 1 > 0:
            self.posX -= self.speedX

    def changePosRight(self):
        if self.posX + 1 <= self.map.x - 1:
            self.posX += self.speedX

    def update(self):
        keyboard.on_press_key("A", self.changePosLeft)
        keyboard.on_press_key("D", self.changePosRight)
        self.map.set_char(self.posX, self.map.y - 1, self.char)
        self.map.set_char(self.posX + 1, self.map.y - 1, self.char)
        self.map.set_char(self.posX - 1, self.map.y - 1, self.char)


class Ball:
    def __init__(self, paddle: Paddle) -> None:
        self.speedX = 1
        self.speedY = -1

        self.posX = 0
        self.posY = 20 - 7
        self.p = paddle

    def draw_on(self, map: Board):
        map.set_char(self.posX, self.posY, "O")

    def update_pos(self, map: Board):
        self.draw_on(map)
        if self.posX == 0 or self.posX == map.x - 1:
            self.speedX = -self.speedX
        if self.posY == 0 or self.posY == map.y - 1:
            self.speedY = -self.speedY
        if self.posY == map.y - 2 and self.p.posX - 1 <= self.posX <= self.p.posX + 1:
            self.speedY = -self.speedY
        self.posX -= self.speedX
        self.posY -= self.speedY


m = Board(15, 20)

m.clear()

time.sleep(0.1)
p = Paddle(m)
ball = Ball(p)
ball.draw_on(m)

while True:
    os.system("cls")
    m.clear()

    ball.update_pos(m)
    p.update()
    print(m)

    time.sleep(0.5)
