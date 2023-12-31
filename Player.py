import arcade


class Player(arcade.Sprite):
    def __init__(self, is_host, role, name, filename, sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.cards = arcade.SpriteList()
        self.name = name
        self.is_host = is_host
        self.role = role
        self.is_distributed = False
        self.time = 0
        self.point = 100
        self.bid = 10
        self.balance = 1000
        self.ready = False

    def bet(self, b):
        self.bid = b

    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        for card in self.cards:
            card.draw()
        arcade.draw_text(self.name, self.center_x + 50, self.center_y + 15, arcade.color.WHITE, 14)
        arcade.draw_text("Bet: " + str(self.bid) + "$", self.center_x + 50, self.center_y - 5, arcade.color.WHITE, 14)
        arcade.draw_text("Balance: " + str(self.balance) + "$", self.center_x + 50, self.center_y - 30, arcade.color.WHITE, 14)
        if not self.is_distributed and self.time > 0:
            arcade.draw_arc_outline(self.center_x, self.center_y, 55, 55, arcade.color.YELLOW_ROSE
                                    , 0, self.time * 72, 10)
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

    def get_cards_point(self):
        total_point = 0
        for c in self.cards:
            if c.num < 10:
                total_point += c.num
            else:
                total_point += 10
        return total_point
