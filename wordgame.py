from source import *
from random import choice


class WordGame:
    """
    Поле для игры №3 (на словарный запас).
    Смысл игры - угадать слово из 5 букв за 6 попыток. Классический Вордл.

    Attributes:
        word (str): Загаданное слово.
        game_ended (bool): Флаг конца игры.
        grid (list): Таблица введенных букв (в формате 0 - нет в слове,
        1 - есть на другом месте, 2 - есть на том же месте).
        answer (str): Ответ, вводимый игроком.
        letters (list): Таблица введенных букв (в формате букв).
        x (int): x-координата вводимой игроком буквы.
        y (int): y-координата вводимой игроком буквы.
    """

    def __init__(self, word_list):
        """
        Создает поле. Загаданное слово случайно выбирается из списка.
        Все остальные атрибуты нулевые или пустые.

        Args:
            word_list (list): Список возможных слов.
        """
        self.word = choice(word_list)
        self.game_ended = False
        self.grid = [[0 for _ in range(5)] for _ in range(6)]
        self.answer = ""
        self.letters = [["" for _ in range(5)] for _ in range(6)]
        self.x = 0
        self.y = 0

    def draw_field(self, screen):
        """
        Рисует поле на экране. Цвет выбирается по
        соответствующему элементу в self.grid.

        Args:
            screen (pygame.Surface): Экран.
        """
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
        """
        Рисует буквы на экране. Цвет выбирается по
        соответствующему элементу в self.grid.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.
        """
        x, y = 125, 90
        for row in range(6):
            for column in range(5):
                if self.grid[row][column] > 0:
                    color = (0, 0, 0)
                else:
                    color = (255, 255, 255)
                print_ui(screen, myfont, str(self.letters[row][column]), x + 25, y + 25, color)
                x += 52
            y += 52
            x = 125

    def check_answer(self, screen, myfont):
        """
        Проверяет попытку. Если слова нет в словаре -
        сообщает игроку и дает ввести слово еще раз.
        Если есть - проверяет, какие буквы верные.
        Если попытка равна слову - игрок побеждает,
        игра кончается. Если попытка не равна слову
        и была последней - игрок проигрывает, игра
        тоже кончается.

        Args:
            screen (pygame.Surface): Экран.
            myfont (pygame.font.Font): Используемый шрифт.

        Returns:
            str: Строка с одним из 3 возможных исходов: "invalid" (некорректный),
            "correct" (верный), "incorrect" (неверный).
        """
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
