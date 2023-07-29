import random
from Card import *
import arcade

# --- Constants ---
SPRITE_SCALING_CARD = 0.1


class CardsBox(arcade.Sprite):
    def __init__(self):
        super().__init__("./assets/cards/black_joker.png", SPRITE_SCALING_CARD)
        self.cards = arcade.SpriteList()
        self.original_alpha = self.alpha
        for n in range(1, 14):
            for s in ["hearts", "diamonds", "clubs", "spades"]:
                card = Card(n, s, SPRITE_SCALING_CARD)
                card.center_x = 400
                card.center_y = 300
                self.cards.append(card)

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        for card in self.cards:
            card.draw()
        super().draw()

    def get_card(self):
        if len(self.cards) > 0:
            c = random.choice(self.cards)
            self.cards.remove(c)
            return c
        return None

    def on_click(self):
        # Custom effect when the sprite is clicked
        self.alpha = 100  # Change sprite transparency

    def reset(self):
        # Reset the sprite to its original state
        self.alpha = self.original_alpha
