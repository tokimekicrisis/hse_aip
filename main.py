from source import *
from mathgame import MathGame, questions
from calcgame import CalcGame
from wordgame import WordGame
from spellgame import SpellGame


def show_menu():
    """
    Показывает главное меню.

    Returns:
        tuple: Кнопки главного меню для дальнейшего использования.
    """
    screen.fill((0, 0, 0))
    print_ui(screen, title_font, "РАЗВИВАШКИ", 250, 40, (0, 255, 0))
    print_ui(screen, text_font, "Мини-игры по математике и", 250, 70, (255, 255, 255))
    print_ui(screen, text_font, "русскому языку для детей", 250, 90, (255, 255, 255))
    mt1 = Button("Знание свойств чисел", 125, 200, 175, 150)
    mt2 = Button("Навыки простого счёта", 375, 200, 175, 150)
    ru1 = Button("Словарный запас (угадайка)", 125, 375, 175, 150)
    ru2 = Button("Орфография (безударные гласные)", 375, 375, 175, 150)
    btns = (mt1, mt2, ru1, ru2)
    for btn in btns:
        btn.display(screen, text_font, pos)
    return btns


def start_game(state):
    """
    Начинает игру.

    Args:
        state (str): Тип игры, которую надо начать.

    Returns:
        MathGame, CalcGame, WordGame или SpellGame в зависимости от нужной игры.
    """

    screen.fill((0, 0, 0))
    if state == "math1":
        fld = MathGame()
        fld.refresh(screen, text_font)
        print_ui(screen, text_font, ("Счёт: " + str(fld.score)).rjust(11), 400, 475, (255, 255, 255))
        print_ui(screen, text_font, "Жизней: " + str(fld.lives), 85, 475, (255, 255, 255))
        return fld
    elif state == "math2":
        fld = CalcGame()
        fld.refresh(screen, text_font, number_font)
        print_ui(screen, text_font, ("Счёт: " + str(fld.score)).rjust(11), 400, 475, (255, 255, 255))
        print_ui(screen, text_font, "Жизней: " + str(fld.lives), 85, 475, (255, 255, 255))
        return fld
    elif state == "rus1":
        with open("resources/words.txt", "r", encoding="utf-8") as f:
            fld = WordGame(f.readlines())
        print_ui(screen, text_font, "Угадай слово за 6 попыток!", 250, 60, (255, 255, 255))
        return fld
    elif state == "rus2":
        fld = SpellGame()
        print_ui(screen, text_font, ("Счёт: " + str(fld.score)).rjust(11), 400, 475, (255, 255, 255))
        print_ui(screen, text_font, "Жизней: " + str(fld.lives), 85, 475, (255, 255, 255))
        print_ui(screen, text_font, "Какая буква пропущена", 250, 70, (255, 255, 255))
        print_ui(screen, text_font, "во всех трех словах?", 250, 95, (255, 255, 255))
        return fld


def game_pause():
    """
    Показывает экран паузы.

    Returns:
        tuple: Кнопка меню и кнопка продолжения игры.
    """
    screen.fill((0, 0, 0))
    print_ui(screen, title_font, "Пауза", 250, 150, (255, 255, 255))
    menu_btn = Button("Меню", 250, 300, 200, 50)
    continue_btn = Button("Продолжить", 250, 400, 200, 50)
    menu_btn.display(screen, text_font, pos)
    continue_btn.display(screen, text_font, pos)
    return menu_btn, continue_btn


def game_over(scr):
    """
    Показывает экран конца игры.

    Args:
        scr (int): Счет игрока.

    Returns:
        Button: Кнопка главного меню.
    """
    screen.fill((0, 0, 0))
    print_ui(screen, title_font, "Игра окончена!", 250, 150, (255, 255, 255))
    print_ui(screen, text_font, "Твой счёт: " + str(scr), 250, 200, (255, 255, 255))
    menu_btn = Button("Меню", 250, 400, 200, 50)
    menu_btn.display(screen, text_font, pos)
    return menu_btn


def game_rules(state):
    """
    Показывает экран правил игры.

    Args:
        state (str): Вид игры, правила которой нужны

    Returns:
        Button: Кнопка перехода к игре.
    """
    screen.fill((0, 0, 0))
    print_ui(screen, title_font, "Правила", 250, 50, (255, 255, 255))
    text = rules[state]
    for num in range(len(text)):
        print_ui(screen, text_font, text[num], 250, 125 + num * 25, (255, 255, 255))
    play_btn = Button("Играть", 250, 400, 200, 50)
    play_btn.display(screen, text_font, pos)
    return play_btn


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Развивашки')
    clock = pygame.time.Clock()

    text_font = pygame.font.Font("resources/Monocraft.otf", 20)
    title_font = pygame.font.Font("resources/Monocraft.otf", 40)
    number_font = pygame.font.Font("resources/Monocraft.otf", 30)
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    game_state = "menu"
    prev_state = "menu"
    score, rounds = 0, 0
    counter, field = None, None

    running = True
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if game_state in ("math1", "math2", "rus1", "rus2"):
                            prev_state = game_state
                            game_state = "pause"

                if game_state == "menu":
                    buttons = show_menu()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons[0].hover(pos):
                            prev_state = "math1"
                            game_state = "rules"
                        elif buttons[1].hover(pos):
                            prev_state = "math2"
                            game_state = "rules"
                        elif buttons[2].hover(pos):
                            prev_state = "rus1"
                            game_state = "rules"
                        elif buttons[3].hover(pos):
                            prev_state = "rus2"
                            game_state = "rules"

                if game_state == "rules":
                    play = game_rules(prev_state)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play.hover(pos):
                            prev_state, game_state = "menu", prev_state
                            if game_state != "rus1":
                                rounds = 0
                                if game_state == "rus2":
                                    counter = Counter(10)
                                else:
                                    counter = Counter(30)
                            field = start_game(game_state)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            prev_state, game_state = "menu", "menu"

                if game_state == "gameover":
                    menu_return = game_over(score)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if menu_return.hover(pos):
                            game_state = "menu"

                if game_state == "pause":
                    buttons = game_pause()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons[0].hover(pos):
                            game_state = "menu"
                        elif buttons[1].hover(pos):
                            screen.fill((0, 0, 0))
                            game_state = prev_state
                            if game_state != "rus1":
                                print_ui(screen, text_font, ("Счёт: " + str(field.score)).rjust(11), 400, 475,
                                         (255, 255, 255))
                                print_ui(screen, text_font, "Жизней: " + str(field.lives), 85, 475, (255, 255, 255))
                            if game_state == "math1":
                                field.draw_field(screen)
                                field.draw_numbers(screen, text_font)
                                print_ui(screen, text_font, questions[field.question], 250, 60, (255, 255, 255))
                            elif game_state == "math2":
                                print_ui(screen, text_font, "Как можно представить число:", 250, 60, (255, 255, 255))
                                print_ui(screen, title_font, str(field.current), 250, 100, (0, 0, 255))
                            elif game_state == "rus1":
                                print_ui(screen, text_font, "Угадай слово за 6 попыток!", 250, 60, (255, 255, 255))
                            elif game_state == "rus2":
                                print_ui(screen, text_font, "Какая буква пропущена", 250, 70, (255, 255, 255))
                                print_ui(screen, text_font, "во всех трех словах?", 250, 95, (255, 255, 255))

                if game_state == "math1":
                    counter.display(screen, number_font)
                    field.draw_field(screen)
                    field.draw_numbers(screen, text_font)
                    if event.type == pygame.USEREVENT:
                        counter.go_down()
                        if counter.time == 0:
                            if len(field.selected) == 0:
                                field.lives -= 1
                                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 200, 100))
                                print_ui(screen, text_font, "Жизней: " + str(field.lives), 85, 475, (255, 255, 255))
                            field.refresh(screen, text_font)
                            if rounds < 15:
                                rounds += 1
                            counter = Counter(30 - rounds // 3 * 5)
                            field.multiplier = rounds // 3 + 1
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            field.select(screen, text_font)
                        else:
                            field.move_player(event.key)
                    if field.answers == field.selected:
                        field.refresh(screen, text_font)
                        if rounds < 15:
                            rounds += 1
                        counter = Counter(30 - rounds // 3 * 5)
                        field.multiplier = rounds // 3 + 1
                    if field.lives == 0:
                        game_state = "gameover"
                        score = field.score

                if game_state == "math2":
                    counter.display(screen, number_font)
                    buttons = field.display_game(screen, text_font, pos)
                    if event.type == pygame.USEREVENT:
                        counter.go_down()
                        if counter.time == 0:
                            if len(field.selected) == 0:
                                field.lives -= 1
                                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 200, 100))
                                print_ui(screen, text_font, "Жизней: " + str(field.lives), 85, 475, (255, 255, 255))
                            field.refresh(screen, text_font, number_font)
                            if rounds < 15:
                                rounds += 1
                            counter = Counter(30 - rounds // 3 * 5)
                            field.multiplier = rounds // 3 + 1
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in buttons:
                            if i.hover(pos):
                                if not (field.answer[-1] in "+-/* " and i.text in "+-/*"):
                                    field.answer += i.text
                                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 125, 500, 50))
                                    print_ui(screen, number_font, field.answer[1:], 250, 150, (255, 255, 255))
                                    break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            field.check_answer(screen, text_font)
                    if field.lives == 0:
                        game_state = "gameover"
                        score = field.score

                if game_state == "rus1":
                    field.draw_field(screen)
                    field.draw_letters(screen, text_font)
                    if event.type == pygame.KEYDOWN:
                        if not field.game_ended:
                            if event.key == pygame.K_RETURN and len(field.answer) == 5:
                                result = field.check_answer(screen, text_font)
                                if result != "invalid":
                                    field.y += 1
                                    if result == "correct" or (result == "incorrect" and field.y == 6):
                                        field.game_ended = True
                                else:
                                    field.letters[field.y] = ["" for _ in range(5)]
                                field.answer = ""
                                field.x = 0
                            elif event.key == pygame.K_BACKSPACE:
                                if len(field.answer) > 0:
                                    field.letters[field.y][field.x - 1] = ""
                                    field.answer = field.answer[:-1]
                                    field.x -= 1
                            else:
                                key = event.unicode
                                if key and key.lower() in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" and len(field.answer) < 5:
                                    field.letters[field.y][field.x] = key.upper()
                                    field.x += 1
                                    field.answer += key

                if game_state == "rus2":
                    counter.display(screen, number_font)
                    if event.type == pygame.USEREVENT:
                        counter.go_down()
                        if counter.time == 0:
                            field.lives -= 1
                            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 200, 100))
                            print_ui(screen, text_font, "Жизней: " + str(field.lives), 85, 475, (255, 255, 255))
                            field.refresh()
                            if rounds < 8:
                                rounds += 1
                                counter = Counter(10)
                            else:
                                counter = Counter(5)
                                field.multiplier = 3
                    field.print_words(screen, text_font)
                    if event.type == pygame.KEYDOWN:
                        key = event.unicode
                        if key and key.lower() in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
                            if field.check_answer(screen, number_font, text_font, key):
                                field.refresh()
                                if rounds < 8:
                                    rounds += 1
                                    counter = Counter(10)
                                else:
                                    counter = Counter(5)
                                    field.multiplier = 3
                    if field.lives == 0:
                        game_state = "gameover"
                        score = field.score

        pygame.display.flip()
    clock.tick(15)

pygame.quit()
