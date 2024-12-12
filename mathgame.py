from source import *
from random import randint

def find_correct(q, num):
    """
    Определяет, является ли число правильным ответом на данный вопрос.

    Args:
        q (int): ID вопроса.
        num (int): Число.

    Returns:
        bool: True, если является, False, если нет.
    """
    if q == 0:
        return num % 2 == 0
    if q == 1:
        return num % 2 == 1
    if q == 2:
        return num % 5 == 0
    if q == 3:
        return num == 7 == 0
    if q == 4:
        return num in {2, 3, 5, 7, 11, 13, 17,
                       19, 23, 29, 31, 37, 41,
                       43, 47, 53, 59, 61, 67,
                       71, 73, 79, 83, 89, 97}
    if q == 5:
        return num > 50
    if q == 6:
        return num in {1, 4, 9, 16, 25, 36, 49, 64, 81, 100}
    if q == 7:
        return num < 10
    if q == 8:
        return num % 3 == 0
    if q == 9:
        return num % 4 == 0


class MathGame:
    """
    Поле для игры №1 (на знание свойств чисел).

    Attributes:
        numbers (list): Числа на поле.
        x (int): x-координата позиции игрока.
        y (int): y-координата позиции игрока.
        question (int): ID вопроса.
        answers (set): Множество координат ячеек с числами, удовлетворяющими вопросу.
        selected (set): Множество координат уже выбранных игроком чисел.
        lives (int): Количество остающихся жизней.
        score (int): Счет.
        multiplier (int): Множитель, на который домножаются очки игрока. Увеличивается с продолжительностью игры.
    """

    def __init__(self):
        """
        Создает новое поле. Почти все атрибуты нулевые или пустые, жизней 5, множитель равен 1.
        """
        self.numbers = []
        self.x, self.y = 0, 0
        self.question = 0
        self.answers = set()
        self.selected = set()
        self.lives = 5
        self.score, self.multiplier = 0, 1

    def set_answers(self):
        """
        Проходит по всему полю и устанавливает правильные ответы.
        """
        self.answers = set()
        for i in range(5):
            for j in range(5):
                if find_correct(self.question, self.numbers[i][j]):
                    self.answers.add((i, j))

    def refresh(self, screen, myfont):
        """
        Обновляет данные (генерирует новые числа и новый вопрос,
        создает пустое множество выбранных ячеек, устанавливает
        верные ответы), и выводит новый вопрос.
        По факту начинает новый раунд.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.
        """
        self.numbers = [[randint(1, 100) for _ in range(5)] for _ in range(5)]
        self.answers = set()
        while len(self.answers) == 0:
            self.question = randint(0, 9)
            self.set_answers()
        self.selected = set()
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 500, 100))
        print_ui(screen, myfont, questions[self.question], 250, 60, (255, 255, 255))

    def draw_field(self, screen):
        """
        Рисует поле на экране. Если ячейка уже была выбрана и
        является правильной - фон зеленый. Если нет: если игрок
        сейчас на ней стоит - фон желтый, если нет - нет фона.

        Args:
            screen (pygame.Surface): Экран.
        """
        x, y = 125, 125
        for row in range(5):
            for column in range(5):
                if (row, column) in self.selected and (row, column) in self.answers:
                    color = (0, 255, 0)
                elif row == self.x and column == self.y:
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
        """
        Рисует числа на поле. Если игрок стоит на ячейке -
        текст черный, если нет - текст белый.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.
        """
        x, y = 125, 125
        for row in range(5):
            for column in range(5):
                if row == self.x and column == self.y:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)
                print_ui(screen, myfont, str(self.numbers[row][column]), x + 25, y + 25, color)
                y += 52
            x += 52
            y = 125

    def move_player(self, event):
        """
        Смотрит, на какую клавишу нажал игрок. Если клавиша -
        стрелочка, то двигает игрока соответственно.

        Args:
            event (pygame.Event): Событие (в данном случае нажатие клавиши).
        """
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
        """
        Выбор ячейки.
        Если ячейка есть в множестве правильных ответов - игроку начисляются
        очки, ячейка отмечается зеленым и добавляется в множество уже выбранных.
        Если ячейка правильная, но уже была выбрана - игроку дается об этом знать.
        Если ячейка неправильная - игрок теряет одну жизнь.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.

        Returns:
            bool: True, если ответ правильный, False, если неправильный.
        """
        position = (self.x, self.y)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(315, 435, 200, 30))
        if position in self.answers:
            if position not in self.selected:
                pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.x * 50 + 125 + (1 + self.x) * 2,
                                                                  self.y * 50 + 125 + (1 + self.y) * 2, 46, 46))
                self.selected.add(position)
                self.score += 50 * self.multiplier
                print_ui(screen, myfont, "  Правильно!", 400, 450, (0, 255, 0))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(280, 460, 200, 50))
                print_ui(screen, myfont, ("Счёт: " + str(self.score)).rjust(11), 400, 475, (255, 255, 255))
                return True
            else:
                print_ui(screen, myfont, "Уже выбрано!", 400, 450, (125, 125, 125))
        else:
            print_ui(screen, myfont, "Неправильно!", 400, 450, (255, 0, 0))
            self.lives -= 1
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 200, 100))
            print_ui(screen, myfont, "Жизней: " + str(self.lives), 85, 475, (255, 255, 255))
            return False


questions = {0: "Выбери все четные числа!",
             1: "Выбери все нечетные числа!",
             2: "Выбери все числа, кратные 5!",
             3: "Выбери все числа, кратные 7!",
             4: "Выбери все простые числа!",
             5: "Выбери все числа, большие 50!",
             6: "Выбери все числа-квадраты!",
             7: "Выбери все однозначные числа!",
             8: "Выбери все числа, кратные 3!",
             9: "Выбери все числа, кратные 4!"}  # словарь вопросов
