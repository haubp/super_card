import arcade


class Card(arcade.Sprite):
    def __init__(self, n, s, sprite_scaling):
        super().__init__("./assets/cards/back.png", sprite_scaling)
        self.num = n
        self.suit = s
        self.frontImage = arcade.load_texture("./assets/cards/" + str(n) + "_of_" + s + ".png")
        self.backImage = arcade.load_texture("./assets/cards/back.png")
        self.isShow = False

    def toggle(self):
        if self.isShow:
            self.texture = self.backImage
        else:
            self.texture = self.frontImage
