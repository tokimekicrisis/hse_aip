import pygame
from random import randint, choice

def print_ui(screen, myfont, text, x, y, color):
    line = myfont.render(text, False, color)
    text_rect = line.get_rect(center=(x, y))
    screen.blit(line, text_rect)

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.width, self.height = w, h
        self.btn = pygame.Rect(0, 0, w, h)
        self.btn.center = (x, y)
        self.x, self.y = x, y
        self.left, self.top = self.btn.left, self.btn.top

    def hover(self, position):
        if self.left < position[0] < self.left + self.width:
            if self.top < position[1] < self.top + self.height:
                return True
        return False

    def display(self, screen, myfont, pos):
        if self.hover(pos):
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)
        txt = self.text.split()
        for i in range(len(txt)):
            if len(txt) == 1:
                print_ui(screen, myfont, txt[i], self.x, self.y, color)
            else:
                print_ui(screen, myfont, txt[i], self.x, self.y + 25 * (i - 1), color)
        pygame.draw.rect(screen, color, self.btn, 2)