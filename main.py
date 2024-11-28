import pygame
from mathgame import MathField, print_ui


# GAME STATES: "math1", "math2", "rus1", "rus2", "menu", "gameover"

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.width, self.height = w, h
        self.btn = pygame.Rect(0, 0, w, h)
        self.btn.center = (x, y)
        self.left, self.top = self.btn.left, self.btn.top

    def hover(self, position):
        if self.left < position[0] < self.left + self.width:
            if self.top < position[1] < self.top + self.height:
                return True
        return False

    def display(self):
        if self.hover(pos):
            color = (255, 255, 0)
        else:
            color = (255, 255, 255)
        txt = text_font.render(self.text, False, color)
        pygame.draw.rect(screen, color, self.btn, 1)
        text_rect = txt.get_rect(center=self.btn.center)
        screen.blit(txt, text_rect)


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
        line = number_font.render(str(self.time).ljust(2), False, color)
        text_rect = line.get_rect(center=(45, 450))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 200, 63))
        screen.blit(line, text_rect)

def show_menu():
    screen.fill((0, 0, 0))
    line = title_font.render("РАЗВИВАШКИ", False, (255, 255, 255))
    text_rect = line.get_rect(center=(250, 60))
    screen.blit(line, text_rect)
    mt1 = Button("test", 250, 250, 100, 100)
    mt1.display()
    mt2, ru1, ru2 = 0, 0, 0
    return mt1, mt2, ru1, ru2

def start_game(state):
    if state == "math1":
        field = MathField()
        field.refresh(screen, text_font)
        print_ui(screen, text_font, "Счёт: " + str(field.score).zfill(5), 400, 475)
        print_ui(screen, text_font, "Жизней: " + str(field.lives), 85, 475)
        return field

def game_over(score):
    screen.fill((0, 0, 0))
    line1 = title_font.render("Игра окончена!", False, (255, 255, 255))
    line2 = text_font.render("Твой счёт: " + str(score), False, (255, 255, 255))
    menu_btn = Button("Главное меню", 250, 400, 200, 100)
    menu_btn.display()
    text_rect1 = line1.get_rect(center=(250, 150))
    text_rect2 = line2.get_rect(center=(250, 200))
    screen.blit(line1, text_rect1)
    screen.blit(line2, text_rect2)
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
    pygame.time.set_timer(pygame.USEREVENT, 1000) # таймер для математических игр

    game_state = "menu"

    running = True
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False # если пользователь нажал крестик, игра кончается
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
                            field = start_game(game_state)
                            rounds = 0
                            counter = Counter(30)
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
                                print_ui(screen, text_font, "Жизней: " + str(field.lives), 85, 475)
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
        pygame.display.flip()
    clock.tick(15)

pygame.quit()
