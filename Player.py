import arcade


class Player(arcade.Sprite):
    def __init__(self, name, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.cards = arcade.SpriteList()
        self.name = name

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        for card in self.cards:
            card.draw()
        arcade.draw_text(self.name, self.center_x + 50, self.center_y, arcade.color.WHITE, 14)
        super().draw()

    def update(self):
        for index, card in enumerate(self.cards):
            if self.center_y > 300:
                if card.center_y < self.center_y - 70:
                    card.center_y += 10
                elif card.center_y > self.center_y - 70:
                    card.center_y -= 10
            else:
                if card.center_y < self.center_y + 70:
                    card.center_y += 10
                elif card.center_y > self.center_y + 70:
                    card.center_y -= 10

            if card.center_x < self.center_x + index * 10:
                card.center_x += 10
            elif card.center_x > self.center_x + index * 10:
                card.center_x -= 10

    def add_card(self, card):
        if card is not None:
            self.cards.append(card)

    def show(self):
        print("Card list of ", self.name)
        for item in self.cards:
            print(item.num, item.suit)

    def get_cards_point(self):
        total_point = 0
        for c in self.cards:
            if c.num < 10:
                total_point += c.num
            else:
                total_point += 10
        return total_point
