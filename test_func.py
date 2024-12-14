import unittest
from unittest.mock import patch
from source import *
import main

pygame.init()

@patch('main.screen', pygame.display.set_mode((500, 500)))
@patch('main.text_font', pygame.font.Font("resources/Monocraft.otf", 20))
@patch('main.title_font', pygame.font.Font("resources/Monocraft.otf", 40))
@patch('main.number_font', pygame.font.Font("resources/Monocraft.otf", 30))
class Test(unittest.TestCase):
    def test_menu_buttons(self):
        self.assertTrue(all(type(i) == Button for i in main.show_menu()))
        self.assertEqual(len(main.show_menu()), 4)

    def test_start_game(self):
        self.assertTrue(type(main.start_game("math1")) == main.MathGame)
        self.assertTrue(type(main.start_game("math2")) == main.CalcGame)
        self.assertTrue(type(main.start_game("rus1")) == main.WordGame)
        self.assertTrue(type(main.start_game("rus2")) == main.SpellGame)

    def test_math_select_correct(self):
        field = main.MathGame()
        field.answers = {(0, 0)}
        field.x, field.y = 0, 0
        self.assertTrue(field.select(main.screen, main.text_font))

    def test_math_select_wrong(self):
        field = main.MathGame()
        field.answers = {(0, 0)}
        field.x, field.y = 1, 0
        self.assertFalse(field.select(main.screen, main.text_font))

    def test_calc_check_correct(self):
        field = main.CalcGame()
        field.answer = " 2+2"
        field.current = 4
        self.assertTrue(field.check_answer(main.screen, main.text_font))

    def test_calc_check_wrong(self):
        field = main.CalcGame()
        field.answer = " 2+2"
        field.current = 5
        self.assertFalse(field.check_answer(main.screen, main.text_font))

    def test_calc_check_error(self):
        field = main.CalcGame()
        field.answer = " 2/0"
        field.current = 4
        self.assertFalse(field.check_answer(main.screen, main.text_font))

    def test_calc_check_unknown_error(self):
        field = main.CalcGame()
        field.answer = "вообще-то это невозможно, но..."
        field.current = 4
        self.assertFalse(field.check_answer(main.screen, main.text_font))

    def test_word_check_correct(self):
        with open("resources/words.txt", "r", encoding="utf-8") as f:
            field = main.WordGame(f.readlines())
        field.answer = "слово"
        field.word = "слово\n"
        self.assertEqual(field.check_answer(main.screen, main.text_font), "correct")

    def test_word_check_wrong(self):
        with open("resources/words.txt", "r", encoding="utf-8") as f:
            field = main.WordGame(f.readlines())
        field.answer = "волос"
        field.word = "слово\n"
        self.assertEqual(field.check_answer(main.screen, main.text_font), "incorrect")

    def test_word_check_invalid(self):
        with open("resources/words.txt", "r", encoding="utf-8") as f:
            field = main.WordGame(f.readlines())
        field.answer = "абоба"
        field.word = "слово\n"
        self.assertEqual(field.check_answer(main.screen, main.text_font), "invalid")

    def test_spell_check_correct(self):
        field = main.SpellGame()
        field.letter = "а"
        self.assertTrue(field.check_answer(main.screen, main.title_font, main.text_font, "а"))

    def test_spell_check_wrong(self):
        field = main.SpellGame()
        field.letter = "а"
        self.assertFalse(field.check_answer(main.screen, main.title_font, main.text_font, "о"))
