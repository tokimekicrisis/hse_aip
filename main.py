from methods import *
from mathgame import MathGame
from calcgame import CalcGame


# GAME STATES: "math1", "math2", "rus1", "rus2", "menu", "gameover", "pause"

class Counter:
    def __init__(self, time):
        self.time = time

    def go_down(self):
        self.time -= 1

    def display(self):
        if self.time > 5:
            color = (255, 255, 255)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 200, 63))
        print_ui(screen, number_font, str(self.time).ljust(2), 45, 450, color)


def show_menu():
    screen.fill((0, 0, 0))
    print_ui(screen, title_font, "РАЗВИВАШКИ", 250, 40, (0, 255, 0))
    print_ui(screen, text_font, "Мини-игры по математике и", 250, 70, (255, 255, 255))
    print_ui(screen, text_font, "русскому языку для детей", 250, 90, (255, 255, 255))
    mt1 = Button("Знание свойств чисел", 125, 200, 175, 150)
    mt2 = Button("Навыки простого счёта", 375, 200, 175, 150)
    ru1 = Button("", 125, 375, 175, 150)
    ru2 = Button("", 375, 375, 175, 150)
    btns = (mt1, mt2, ru1, ru2)
    for i in btns:
        i.display(screen, text_font, pos)
    return btns


def start_game(state):
    screen.fill((0, 0, 0))
    if state == "math1":
        fld = MathGame()
        fld.refresh(screen, text_font)
        print_ui(screen, text_font, ("Счёт: " + str(fld.score)).rjust(11), 400, 475, (255, 255, 255))
        print_ui(screen, text_font, "Жизней: " + str(fld.lives), 85, 475, (255, 255, 255))
        return fld
    elif state == "math2":
        fld = CalcGame()
        fld.display_calc(screen, text_font, pos)
        print_ui(screen, text_font, ("Счёт: " + str(fld.score)).rjust(11), 400, 475, (255, 255, 255))
        print_ui(screen, text_font, "Жизней: " + str(fld.lives), 85, 475, (255, 255, 255))
        return fld


def game_over(scr):
    screen.fill((0, 0, 0))
    print_ui(screen, title_font, "Игра окончена!", 250, 150, (255, 255, 255))
    print_ui(screen, text_font, "Твой счёт: " + str(scr), 250, 200, (255, 255, 255))
    menu_btn = Button("Главное меню", 250, 400, 200, 100)
    menu_btn.display(screen, text_font, pos)
    return menu_btn


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Развивашки')
    clock = pygame.time.Clock()

    text_font = pygame.font.Font("resources/Monocraft.otf", 20)
    title_font = pygame.font.Font("resources/Monocraft.otf", 40)
    number_font = pygame.font.Font("resources/Monocraft.otf", 30)
    pygame.time.set_timer(pygame.USEREVENT, 1000)  # таймер для математических игр

    game_state = "menu"

    running = True
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False  # если пользователь нажал крестик, игра кончается
            else:
                if game_state == "gameover":
                    menu_return = game_over(score)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if menu_return.hover(pos):
                            game_state = "menu"

                if game_state == "menu":
                    buttons = show_menu()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if buttons[0].hover(pos):
                            game_state = "math1"
                            rounds = 0
                            counter = Counter(30)
                        elif buttons[1].hover(pos):
                            game_state = "math2"
                        field = start_game(game_state)

                if game_state == "math1":
                    counter.display()
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
                    field.display_calc(screen, text_font, pos)

        pygame.display.flip()
    clock.tick(15)

pygame.quit()
