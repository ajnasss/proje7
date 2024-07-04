import unittest
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
from testt import MenuScreen, Game, Player, PokemonCard, Deck

class TestPokemonGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.menu_screen = MenuScreen(self.root)
        self.menu_screen.root.withdraw()  # Pencereyi görünmez yaparak test etmek için

    def tearDown(self):
        if self.menu_screen.root.winfo_exists():
            self.menu_screen.root.destroy()

    def test_menu_screen(self):
        # Test menu screen açılıyor mu?
        self.menu_screen.root.deiconify()  # Pencereyi tekrar görünür yap
        self.assertTrue(self.menu_screen.root.winfo_exists())

    def test_start_game_with_computer(self):
        # Bilgisayarla oyun başlatılıyor mu?
        self.menu_screen.choose_computer()
        game_window = self.get_game_window()
        self.assertIsNotNone(game_window)

    def test_start_game_with_player(self):
        # Oyuncuyla oyun başlatılıyor mu?
        self.menu_screen.choose_player()
        game_window = self.get_game_window()
        self.assertIsNotNone(game_window)

    def test_game(self):
        # Oyun işleyişini doğru bir şekilde test etmek
        self.menu_screen.choose_computer()
        game_window = self.get_game_window()
        game = game_window.game

        # Game mekaniklerini test et.
        game.next_round()

    def get_game_window(self):
        game_window = None
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                game_window = widget
                break
        return game_window

if __name__ == "__main__":
    unittest.main()
