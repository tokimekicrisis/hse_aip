from methods import *

class CalcGame():
    def __init__(self):
        self.current = randint(1, 30)
        self.lives = 5
        self.selected = set()
        self.score, self.multiplier = 0, 1

    def check_answer(self, screen, myfont, answer):
        if eval(answer) == self.current:
            if answer not in self.selected:
                self.score += 50 * self.multiplier
                self.selected.add(answer + "=" + str(self.current))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(300, 400, 200, 100))
                print_ui(screen, myfont, ("Счёт: " + str(self.score)).rjust(11), 400, 475, (255, 255, 255))
        else:
            self.lives -= 1
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 200, 100))
            print_ui(screen, myfont, "Жизней: " + str(self.lives), 85, 475, (255, 255, 255))

    def display_calc(self, screen, myfont, pos):
        numbers = ("123", "456", "789", "0")
        signs = "+-/*"
        for i in range(4):
            for j in range(len(numbers[i])):
                num = Button(numbers[i][j], 50 + j * 52, 200 + i * 52, 50, 50)
                num.display(screen, myfont, pos)
            sign = Button(signs[i], 250 + (i % 2) * 52, 200 + (i > 1) * 52, 50, 50)
            sign.display(screen, myfont, pos)

