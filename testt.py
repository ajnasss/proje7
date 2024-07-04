import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from functools import partial

class MenuScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Card Game Menusu")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Secenek seciniz:", font=("Arial", 18))
        self.label.pack(pady=50)

        self.play_with_player_button = tk.Button(root, text="Bilgisayarla Oyna", command=self.choose_player)
        self.play_with_player_button.pack()

        self.play_with_computer_button = tk.Button(root, text="Bilgisayar Bilgisayarla Oynasın", command=self.choose_computer)
        self.play_with_computer_button.pack()

    def choose_player(self):
        self.root.destroy()
        self.start_game(is_computer=False)

    def choose_computer(self):
        self.root.destroy()
        self.start_game(is_computer=True)

    def start_game(self, is_computer=False):
        player1 = Player("Oyuncu")
        if is_computer:
            player2 = Player("Computer 1", is_computer=True)
            player3 = Player("Computer 2", is_computer=True)
            root = tk.Tk()
            game = Game(root, player2, player3, is_computer_vs_computer=True)
        else:
            player2 = Player("Bilgisayar")
            root = tk.Tk()
            game = Game(root, player1, player2)
        root.mainloop()

class PokemonCard:
    def __init__(self, name=None, damage=0, image_path=None):
        self.name = name
        self.damage = damage
        self.image_path = image_path
        self.image = self.load_image(image_path, (150, 200))
        self.small_image = self.load_image(image_path, (100, 133))
        self.back_image = self.load_image("C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/arka.png", (150, 200))
        self.small_back_image = self.load_image("C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/arka.png", (94, 127))

    def load_image(self, path, size):
        if path:
            img = Image.open(path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        return None

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_damage(self):
        return self.damage

    def set_damage(self, damage):
        self.damage = damage

    def get_image(self):
        return self.image

    def get_small_image(self):
        return self.small_image

    def get_back_image(self):
        return self.back_image

    def get_small_back_image(self):
        return self.small_back_image

    def set_image_path(self, image_path):
        self.image_path = image_path
        self.image = self.load_image(image_path, (150, 200))
        self.small_image = self.load_image(image_path, (100, 133))

    def __str__(self):
        return f"{self.name} ({self.damage} damage)"

class Deck:
    def __init__(self):
        self.cards = [
            PokemonCard("Pikachu", 20, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/pikachu.png"),
            PokemonCard("Charmander", 20, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/charmander.png"),
            PokemonCard("Bulbasaur", 50, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/bulbasaur.png"),
            PokemonCard("Squirtle", 30, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/squirtle.png"),
            PokemonCard("Eevee", 30, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/eevee.png"),
            PokemonCard("Jigglypuff", 20, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/jigglypuff.png"),
            PokemonCard("Meowth", 70, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/meowth.png"),
            PokemonCard("Psyduck", 10, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/psyduck.png"),
            PokemonCard("Snorlax", 60, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/snorlax.png"),
            PokemonCard("Mewtwo", 20, "C:/Users/ecena/PycharmProjects/pythonProjectasa/venv/pokemon_karakterler/mewtwo.png")
        ]
        self.shuffle_cards()

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None

    def __len__(self):
        return len(self.cards)

class Player:
    def __init__(self, name=None, is_computer=False):
        self.name = name
        self.is_computer = is_computer
        self.hand = []
        self.score = 0

    def draw_initial_cards(self, deck):
        for _ in range(3):
            self.hand.append(deck.draw_card())

    def play_card(self, index=None):
        if not self.hand:
            return None

        if index is None or index < 0 or index >= len(self.hand):
            return self.hand.pop()

        return self.hand.pop(index)

    def add_score(self, points):
        self.score += points

    def draw_card(self, deck):
        card = deck.draw_card()
        if card:
            self.hand.append(card)

    def get_score(self):
        return self.score

    def __str__(self):
        return self.name

class Game:
    def __init__(self, root, player1, player2, is_computer_vs_computer=False):
        self.root = root
        self.root.title("Pokemon Card Game")
        self.root.geometry("1200x800")

        self.deck = Deck()
        self.deck.shuffle_cards()

        self.player1 = player1
        self.player2 = player2
        self.is_computer_vs_computer = is_computer_vs_computer

        self.player1.draw_initial_cards(self.deck)
        self.player2.draw_initial_cards(self.deck)

        self.selected_card_index = None

        self.player1_images = []
        self.computer_card_image = None

        self.create_widgets()
        self.update_display()

        if self.is_computer_vs_computer:
            self.root.after(1000, self.play_round)

    def create_widgets(self):
        self.player1_frame = tk.Frame(self.root)
        self.player1_frame.pack(pady=10)

        self.side_frame = tk.Frame(self.root)
        self.side_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.computer_frame = tk.Frame(self.root)
        self.computer_frame.pack(side=tk.BOTTOM, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.player1_label = tk.Label(self.player1_frame, text=f"{self.player1.name}'in eli", font=("Arial", 14))
        self.player1_label.grid(row=0, column=0, columnspan=3)

        self.player1_buttons = []
        for i in range(3):
            btn = tk.Button(self.player1_frame, text="", command=partial(self.play_card, i))
            btn.grid(row=1, column=i, padx=10, pady=10)
            self.player1_buttons.append(btn)

        self.play_button = tk.Button(self.button_frame, text="Tur Oyna", command=self.play_round)
        self.play_button.pack()

        self.player1_card_label = tk.Label(self.result_frame, text="", font=("Arial", 14))
        self.player1_card_label.grid(row=0, column=0, padx=10)

        self.vs_label = tk.Label(self.result_frame, text="VS", font=("Arial", 14))
        self.vs_label.grid(row=0, column=1, padx=10)

        self.player2_card_label = tk.Label(self.result_frame, text="", font=("Arial", 14))
        self.player2_card_label.grid(row=0, column=2, padx=10)

        self.round_result_label = tk.Label(self.result_frame, text="", font=("Arial", 14))
        self.round_result_label.grid(row=1, column=0, columnspan=3)

        self.next_round_button = tk.Button(self.result_frame, text="Sonraki Tur", command=self.next_round)
        self.next_round_button.grid(row=2, column=0, columnspan=3)
        self.next_round_button.config(state="disabled")

        self.middle_cards_label = tk.Label(self.side_frame, text="Ortadaki Kartlar", font=("Arial", 14))
        self.middle_cards_label.grid(row=0, column=0, columnspan=4)

        self.middle_cards_buttons = []
        for i in range(4):
            btn = tk.Label(self.side_frame, text="")
            btn.grid(row=1, column=i, padx=10, pady=10)
            self.middle_cards_buttons.append(btn)

        self.computer_hand_label = tk.Label(self.computer_frame, text=f"{self.player2.name}'in eli", font=("Arial", 14))
        self.computer_hand_label.grid(row=0, column=0, columnspan=3)

        self.computer_hand_buttons = []
        for i in range(3):
            btn = tk.Label(self.computer_frame, text="", image=self.player2.hand[0].get_small_back_image())
            btn.grid(row=1, column=i, padx=10, pady=10)
            self.computer_hand_buttons.append(btn)

    def update_display(self):
        self.player1_images = [card.get_image() for card in self.player1.hand]
        for i, card_image in enumerate(self.player1_images):
            self.player1_buttons[i].config(image=card_image, text="", compound="top")

        for i, card in enumerate(self.player2.hand):
            self.computer_hand_buttons[i].config(image=card.get_small_back_image(), text="")

        if any(card.get_small_back_image() for card in self.deck.cards[:4]):
            self.middle_cards_label.grid(row=0, column=0, columnspan=4)
        else:
            self.middle_cards_label.grid_forget()

        for i in range(4):
            if i < len(self.deck.cards):
                card = self.deck.cards[i]
                self.middle_cards_buttons[i].config(image=card.get_small_back_image(), text="")
            else:
                self.middle_cards_buttons[i].config(image="", text="")

    def play_card(self, card_index):
        self.selected_card_index = card_index

    def play_round(self):
        if not self.is_computer_vs_computer and self.selected_card_index is None:
            return

        if len(self.player1.hand) == 0 or len(self.player2.hand) == 0:
            self.end_game()
            return

        if self.is_computer_vs_computer:
            card1 = self.player1.play_card()
            card2 = self.player2.play_card()
        else:
            card1 = self.player1.play_card(self.selected_card_index)
            card2 = self.player2.play_card()

        player1_card_image = card1.get_image()
        player2_card_image = card2.get_image()

        self.player1_card_label.config(image=player1_card_image)
        self.player1_card_label.image = player1_card_image
        self.player2_card_label.config(image=player2_card_image)
        self.player2_card_label.image = player2_card_image

        if card1.get_damage() > card2.get_damage():
            self.round_result_label.config(text=f"{self.player1.name} turu kazanır!")
            self.player1.add_score(1)
        elif card1.get_damage() < card2.get_damage():
            self.round_result_label.config(text=f"{self.player2.name} turu kazanır!")
            self.player2.add_score(1)
        else:
            self.round_result_label.config(text="Berabere!")

        self.vs_label.config(text=f"{card1.get_name()} VS {card2.get_name()}")

        self.play_button.config(state="disabled")
        self.next_round_button.config(state="normal")

        if self.is_computer_vs_computer:
            self.root.after(1000, self.next_round)

    def next_round(self):
        self.selected_card_index = None

        self.player1_card_label.destroy()
        self.player1_card_label = tk.Label(self.result_frame, text="", font=("Arial", 14))
        self.player1_card_label.grid(row=0, column=0, padx=10)

        self.player2_card_label.destroy()
        self.player2_card_label = tk.Label(self.result_frame, text="", font=("Arial", 14))
        self.player2_card_label.grid(row=0, column=2, padx=10)

        self.round_result_label.config(text="")
        self.vs_label.config(text="")

        self.play_button.config(state="normal")
        self.next_round_button.config(state="disabled")

        if len(self.deck.cards) >= 2:
            player_card = self.deck.draw_card()
            self.player1.hand.append(player_card)

            computer_card = self.deck.draw_card()
            self.player2.hand.append(computer_card)

        self.update_display()

        if len(self.deck.cards) == 0 and len(self.player1.hand) == 0 and len(self.player2.hand) == 0:
            self.end_game()
        elif len(self.deck.cards) == 0:
            self.play_round()

        if self.is_computer_vs_computer:
            self.root.after(1000, self.play_round)

    def end_game(self):
        winner = None
        if self.player1.get_score() >= 5:
            winner = self.player1.name
        elif self.player2.get_score() >= 5:
            winner = self.player2.name
        elif self.player1.get_score() > self.player2.get_score():
            winner = self.player1.name
        elif self.player1.get_score() < self.player2.get_score():
            winner = self.player2.name
        else:
            winner = "Kimse. Berabere!"
        messagebox.showinfo("Oyun Bitti", f"Oyun bitti! Kazanan: {winner}")
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    menu = MenuScreen(root)
    root.mainloop()
