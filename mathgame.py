from random import randint
import pygame


def find_correct(q, num):
    if q == 0:
        return num % 2 == 0
    if q == 1:
        return num % 2 == 1
    if q == 2:
        return num % 5 == 0
    if q == 3:
        return num == 7 == 0
    if q == 4:
        return num in [2, 3, 5, 7, 11, 13, 17,
                       19, 23, 29, 31, 37, 41,
                       43, 47, 53, 59, 61, 67,
                       71, 73, 79, 83, 89, 97]
    if q == 5:
        return num > 50
    if q == 6:
        return num in [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    if q == 7:
        return num < 10
    if q == 8:
        return num % 3 == 0
    if q == 9:
        return num % 4 == 0


class MathField:
    def __init__(self, screen):
        self.numbers = []
        self.x, self.y = 0, 0
        self.question = 0
        self.answers = set()
        self.selected = set()
        self.score, self.multiplier = 0, 1
        self.refresh(screen)

    def set_answers(self):
        self.answers = set()
        for i in range(5):
            for j in range(5):
                if find_correct(self.question, self.numbers[i][j]):
                    self.answers.add((i, j))

    def refresh(self, screen):
        self.numbers = [[randint(1, 100) for i in range(5)] for j in range(5)]
        self.question = randint(0, 9)
        self.selected = set()
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 500, 100))
        self.set_answers()

    def draw_field(self, screen):
        x, y = 125, 125
        for row in range(5):
            for column in range(5):
                if (row, column) in self.selected:
                    continue
                if row == self.x and column == self.y:
                    color = (255, 255, 0)
                else:
                    color = (0, 0, 0)
                pygame.draw.rect(screen, color, pygame.Rect(row * 50 + 125 + (1 + row) * 2,
                                                            column * 50 + 125 + (1 + column) * 2, 46, 46))
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 50, 50), 2)
                y += 52
            x += 52
            y = 125

    def draw_numbers(self, screen, myfont):
        x, y = 125, 125
        for row in range(5):
            for column in range(5):
                if row == self.x and column == self.y:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)
                number = myfont.render(str(self.numbers[row][column]), False, color)
                text_rect = number.get_rect(center=(x + 25, y + 25))
                screen.blit(number, text_rect)
                y += 52
            x += 52
            y = 125

    def move_player(self, event):
        if event == pygame.K_UP:
            if self.y == 0:
                self.y = 4
            else:
                self.y -= 1
        elif event == pygame.K_DOWN:
            if self.y == 4:
                self.y = 0
            else:
                self.y += 1
        elif event == pygame.K_RIGHT:
            if self.x == 4:
                self.x = 0
            else:
                self.x += 1
        elif event == pygame.K_LEFT:
            if self.x == 0:
                self.x = 4
            else:
                self.x -= 1

    def select(self, screen, myfont):
        position = (self.x, self.y)
        print(self.answers, self.selected)
        if position in self.answers:
            if position not in self.selected:
                print("Правильно!")
                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(self.x * 50 + 125 + (1 + self.x) * 2,
                                                                  self.y * 50 + 125 + (1 + self.y) * 2, 46, 46))
                self.selected.add(position)
                self.score += 100 * self.multiplier
                self.print_score(screen, myfont)
            else:
                print("Уже выбрано!")
        else:
            print("Неправильно!")

    def print_question(self, screen, myfont):
        line = myfont.render(questions[self.question], False, (255, 255, 255))
        text_rect = line.get_rect(center=(250, 60))
        screen.blit(line, text_rect)

    def print_score(self, screen, myfont):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 500, 100))
        score = myfont.render("Счёт: " + str(self.score), False, (255, 255, 255))
        text_rect = score.get_rect(center=(400, 475))
        screen.blit(score, text_rect)


questions = {0: "Выбери все четные числа!",
             1: "Выбери все нечетные числа!",
             2: "Выбери все числа, кратные 5!",
             3: "Выбери все числа, кратные 7!",
             4: "Выбери все простые числа!",
             5: "Выбери все числа, большие 50!",
             6: "Выбери все числа-квадраты!",
             7: "Выбери все однозначные числа!",
             8: "Выбери все числа, кратные 3!",
             9: "Выбери все числа, кратные 4!"}
