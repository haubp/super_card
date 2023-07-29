import arcade


class Card(arcade.Sprite):
    def __init__(self, n, s, sprite_scaling):
        super().__init__("./assets/cards/" + str(n) + "_of_" + s + ".png", sprite_scaling)
        self.num = n
        self.suit = s
