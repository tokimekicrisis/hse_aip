import sys
import pygame
from mathgame import MathField


class Button:
    def __init__(self, text, w, h):
        self.text = text
        self.center_w, self.center_h = w, h
        txt = text_font.render(self.text, False, (255, 255, 255))
        self.text_rect = txt.get_rect(center=(self.center_w, self.center_h))
        self.text_rect2 = pygame.Rect(0, 0, 180, self.text_rect.height)
        self.text_rect2.center = (self.center_w, self.center_h)
        self.left, self.top, self.width, self.height = \
            self.text_rect2.left, self.text_rect2.top, self.text_rect2.width, self.text_rect2.height

    def hover(self, pos):
        if self.left < pos[0] < self.left + self.width:
            if self.top < pos[1] < self.top + self.height:
                return True
        return False

    def display(self):
        if self.hover(pos):
            txt = text_font.render(self.text, False, (0, 255, 255))
            pygame.draw.rect(screen, (0, 255, 255), self.text_rect2, width=1)
        else:
            txt = text_font.render(self.text, False, (255, 255, 255))
            pygame.draw.rect(screen, (255, 255, 255), self.text_rect2, width=1)
        screen.blit(txt, self.text_rect)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Развивашки')
    clock = pygame.time.Clock()

    number_font = pygame.font.Font("resources/HomeVideo-Regular.otf", 25)
    text_font = pygame.font.Font("resources/HomeVideo-Regular.otf", 25)

    game_state = "math"
    field = MathField(screen)

    running = True
    while running:
        if game_state == "math":
            field.draw_field(screen)
            field.draw_numbers(screen, number_font)
            field.print_question(screen, text_font)
            field.print_score(screen, text_font)
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        field.select(screen, text_font)
                    elif event.key == pygame.K_RETURN:
                        field.refresh(screen)
                    else:
                        field.move_player(event.key)
            if field.answers == field.selected:
                field.refresh(screen)
        pygame.display.flip()
        clock.tick(15)

pygame.quit()
