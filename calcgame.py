from methods import *
from random import randint

class CalcGame:
    """
    Поле для игры №2 (на навыки счета).
    Смысл игры - представить данное число максимальным возможным
    количеством способов с помощью клавиатуры на экране.

    Attributes:
        current (int): Данное число.
        lives (int): Количество остающихся жизней.
        selected (set): Множество уже введенных вариантов ответа.
        answer (str): Ответ, вводимый игроком.
        score (int): Счет.
        multiplier (int): Множитель, на который домножаются очки игрока. Увеличивается с продолжительностью игры.
    """

    def __init__(self):
        """
        Создает поле. Загаданное число - случайно выбранное от 1 до 30.
        Жизней 5, множитель = 1, все остальные атрибуты нулевые или пустые.
        """

        self.current = randint(1, 30)
        self.lives = 5
        self.selected = set()
        self.answer = " "
        self.score, self.multiplier = 0, 1

    def refresh(self, screen, myfont1, myfont2):
        """
        Обновляет данные (генерирует новое число,
        обнуляет множество введенных ответов и
        вводимый ответ), выводит новый вопрос.
        По факту начинает новый раунд.

        Args:
            screen (pygame.Surface): Экран.
            myfont1 (pygame.font.Font): Шрифт для вопроса.
            myfont2 (pygame.font.Font): Шрифт для числа.
        """
        self.current = randint(1, 30)
        self.selected = set()
        self.answer = " "
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, 500, 200))
        print_ui(screen, myfont1, "Как можно представить число:", 250, 60, (255, 255, 255))
        print_ui(screen, myfont2, str(self.current), 250, 100, (0, 0, 255))

    def check_answer(self, screen, myfont):
        """
        Проверяет введенный ответ на правильность.
        Если ответ пустой - ничего не делает.
        Если ответ не пустой - пытается его оценить.
        Если игрок попытался поделить на ноль - выводит предупреждение.
        Если игрок как-то умудрился вызвать еще какое-то исключение -
        выводит общее предупреждение.
        Иначе: если ответ правильный - добавляет его в множество выбранных
        и начисляет игроку очки, если уже использован - выводит
        предупреждение, если неправильный - игрок теряет одну жизнь.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.
        """

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(200, 435, 300, 30))
        if self.answer == " ":
            pass
        else:
            try:
                if eval(self.answer) == self.current:
                    if self.answer not in self.selected:
                        print_ui(screen, myfont, "  Правильно!", 400, 450, (0, 255, 0))
                        self.score += 50 * self.multiplier
                        self.selected.add(self.answer)
                        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(280, 460, 200, 50))
                        print_ui(screen, myfont, ("Счёт: " + str(self.score)).rjust(11), 400, 475, (255, 255, 255))
                    else:
                        print_ui(screen, myfont, "   Уже было!", 400, 450, (125, 125, 125))
                else:
                    print_ui(screen, myfont, "Неправильно!", 400, 450, (255, 0, 0))
                    self.lives -= 1
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 200, 100))
                    print_ui(screen, myfont, "Жизней: " + str(self.lives), 85, 475, (255, 255, 255))
            except ZeroDivisionError:
                print_ui(screen, myfont, "Делить на ноль нельзя!", 350, 450, (255, 0, 0))
            except Exception:
                print_ui(screen, myfont, "Некорректное выражение!", 350, 450, (255, 0, 0))
            self.answer = " "

    def display_game(self, screen, myfont, pos):
        """
        Выводит клавиатуру на экран и возвращает все кнопки для дальнейшего использования.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.
            pos (tuple): Позиция курсора.
        """
        numbers = ("123", "456", "789", "0")
        signs = "+-/*"
        buttons = set()
        for i in range(4):
            for j in range(len(numbers[i])):
                num = Button(numbers[i][j], 50 + j * 52, 230 + i * 52, 50, 50)
                buttons.add(num)
            sign = Button(signs[i], 250 + (i % 2) * 52, 230 + (i > 1) * 52, 50, 50)
            buttons.add(sign)
        for i in buttons:
            i.display(screen, myfont, pos)
        return buttons
