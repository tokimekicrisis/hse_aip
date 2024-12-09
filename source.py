import pygame

def print_ui(screen, myfont, text, x, y, color):
    """
    Выводит текст на экран.

    Args:
        screen (pygame.Surface): Экран.
        myfont (pygame.font.Font): Используемый шрифт.
        text (str): Выводимый текст.
        x (int): x-координата центра прямоугольника текста.
        y (int): y-координата центра прямоугольника текста.
        color (tuple): Цвет текста в формате RGB.
    """

    line = myfont.render(text, False, color)
    text_rect = line.get_rect(center=(x, y))
    screen.blit(line, text_rect)


class Button:
    """
    Кнопка с текстом. При нажатии что-то делает (что именно - задано в main.py).

    Attributes:
        text (str): Текст кнопки.
        x (int): x-координата центра кнопки.
        y (int): y-координата центра кнопки.
        width (int): Ширина кнопки.
        height (int): Высота кнопки.
        btn (pygame.Rect): Прямоугольник кнопки.
        left (int): x-координата левого верхнего угла прямоугольника.
        top (int): y-координата левого верхнего угла прямоугольника.
    """

    def __init__(self, text, x, y, w, h):
        """
        Создает новую кнопку.

        Args:
            text (str): Текст кнопки.
            x (int): x-координата центра кнопки.
            y (int): y-координата центра кнопки.
            w (int): Ширина кнопки.
            h (int): Высота кнопки.
        """

        self.text = text
        self.width, self.height = w, h
        self.btn = pygame.Rect(0, 0, w, h)
        self.btn.center = (x, y)
        self.x, self.y = x, y
        self.left, self.top = self.btn.left, self.btn.top

    def hover(self, position):
        """
        Проверяет, находится ли курсор в данный момент на кнопке.
        Это нужно, чтобы понимать, надо подсвечивать кнопку или нет,
        а также чтобы распознавать нажатие кнопки.

        Args:
            position (tuple): Позиция курсора.

        Returns:
            bool: True, если курсор на кнопке, False, если нет.
        """

        if self.left < position[0] < self.left + self.width:
            if self.top < position[1] < self.top + self.height:
                return True
        return False

    def display(self, screen, myfont, pos):
        """
        Выводит кнопку на экран.
        При необходимости разбивает текст на несколько строк.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.
            pos (tuple): Позиция курсора.
        """

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


class Counter:
    """
    Простой убывающий таймер.

    Attributes:
        time (int): Время на таймере.
    """

    def __init__(self, time):
        """
        Заводит таймер на данное количество секунд.

        Args:
            time (int): Время на таймере (в секундах).
        """
        self.time = time

    def go_down(self):
        """
        Уменьшает время на таймере на 1 сек.
        """
        self.time -= 1

    def display(self, screen, myfont):
        """
        Выводит таймер на экран.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.
        """
        if self.time > 5:
            color = (255, 255, 255)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(25, 415, 50, 50))
        print_ui(screen, myfont, str(self.time).ljust(2), 45, 450, color)


rules = {"math1": ["Выбирай на поле числа,",
                   "соответствующие условию.",
                   "Передвигайся с помощью стрелок,",
                   "выбирай числа с помощью пробела.",
                   "За неправильные ответы либо",
                   "отсутствие ответа ты будешь",
                   "терять жизни!"],

         "math2": ["C помощью клавиш на экране",
                   "введи все возможные способы,",
                   "которыми ты можешь представить",
                   "данное число. Чтобы проверить",
                   "ответ, нажми Enter на клавиатуре.",
                   "За неправильные ответы либо",
                   "отсутствие ответа ты будешь",
                   "терять жизни!"],

         "rus1": ["Какое мы загадали слово? Попробуй",
                  "отгадать! Тебе дано 6 попыток.",
                  "Если буква в твоей попытке есть",
                  "в загаданном слове, но на другом",
                  "месте, она станет желтой. Если на",
                  "правильном месте - зеленой.",
                  "Разрешены только существительные."],

         "rus2": ["На экране показаны три слова с",
                  "пропусками. Какая буква стоит на",
                  "месте пропусков во всех словах?",
                  "Введи ее с помощью клавиатуры.",
                  "За неправильные ответы либо",
                  "отсутствие ответа ты будешь",
                  "терять жизни!"]}
