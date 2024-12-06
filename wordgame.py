import pygame.draw

from source import *
from random import choice


class WordGame:
    def __init__(self, word_list):
        self.word = choice(word_list)
        self.game_ended = False
        self.grid = [[0 for _ in range(5)] for _ in range(6)]
        self.answer = ""
        self.letters = [["" for _ in range(5)] for _ in range(6)]
        self.x = 0
        self.y = 0

    def draw_field(self, screen):
        x, y = 125, 90
        for row in range(6):
            for column in range(5):
                square = self.grid[row][column]
                if square > 0:
                    color = (255 * (square % 2), 255, 0)
                else:
                    color = (0, 0, 0)
                pygame.draw.rect(screen, color, pygame.Rect(column * 50 + 125 + (1 + column) * 2,
                                                            (row - 1) * 50 + 140 + (1 + row) * 2, 46, 46))
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 50, 50), 2)
                x += 52
            y += 52
            x = 125

    def draw_letters(self, screen, myfont):
        x, y = 125, 90
        for row in range(6):
            for column in range(5):
                if row == self.y and column == self.x:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)
                print_ui(screen, myfont, str(self.letters[row][column]), x + 25, y + 25, color)
                x += 52
            y += 52
            x = 125

    def check_answer(self, screen, myfont):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 450, 500, 50))
        self.answer += "\n"
        word_check = False
        with open("resources/words.txt", "r", encoding="utf-8") as f:
            if self.answer in f.readlines():
                word_check = True
        if not word_check:
            print_ui(screen, myfont, "В нашем словаре нет такого слова!", 250, 475, (255, 0, 0))
            return "invalid"
        else:
            for index in range(5):
                if self.answer[index] in self.word:
                    if self.answer[index] == self.word[index]:
                        self.grid[self.y][index] = 2
                    else:
                        self.grid[self.y][index] = 1
            if self.answer == self.word:
                print_ui(screen, myfont, "Молодец, ты угадал слово!", 250, 450, (0, 255, 0))
                print_ui(screen, myfont, "Правильный ответ: " + self.word[:-1].upper(), 250, 475, (0, 255, 0))
                return "correct"
            else:
                if self.y == 5:
                    print_ui(screen, myfont, "Очень жаль, ты не угадал слово!", 250, 450, (255, 0, 0))
                    print_ui(screen, myfont, "Правильный ответ: " + self.word[:-1].upper(), 250, 475, (255, 0, 0))
            return "incorrect"
